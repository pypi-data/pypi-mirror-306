#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/25 19:03
# @Author  : 兵
# @email    : 1747193328@qq.com

import math
import os.path

import numpy as np
from ase import Atoms

from ase.io import write as ase_write
from NepTrain.io.vasp import VaspInput
from NepTrain import utils, Config,module_path
atoms_index=1

@utils.iter_path_to_atoms(["*.vasp","*.xyz"],show_progress=True,
                 desc="VASP计算进度",unit="job")
def calculate_vasp(atoms:Atoms,argparse):
    global atoms_index
    vasp = VaspInput()
    if argparse.incar is not None:
        vasp.read_incar(argparse.incar)
    else:
        vasp.read_incar(os.path.join(module_path,"io/vasp/INCAR"))
    directory=os.path.join(argparse.directory,f"{atoms_index}-{atoms.symbols}")
    atoms_index+=1
    command=f"{Config.get('environ','mpirun_path')} -n {argparse.n_cpu} {Config.get('environ','vasp_path')}"

    a,b,c,alpha, beta, gamma=atoms.get_cell_lengths_and_angles()

    vasp.set(kspacing=argparse.kspacing,
             directory=directory,
             command=command,
            kpts=(math.ceil(argparse.kpoints[0]/a)  ,
                  math.ceil(argparse.kpoints[1]/b)  ,
                  math.ceil(argparse.kpoints[2]/b) ),
             gamma=argparse.use_gamma,
             )
    vasp.calculate(atoms,('energy'))
    atoms.calc=vasp._xml_calc
    xx, yy, zz, yz, xz, xy = -vasp.results['stress'] * atoms.get_volume()  # *160.21766
    atoms.info['virial'] = np.array([(xx, xy, xz), (xy, yy, yz), (xz, yz, zz)])
    #这里没想好怎么设计config的格式化  就先使用原来的
    if "Config_type" not in atoms.info:

        atoms.info['Config_type'] = "NepTrain scf "
    atoms.info['Weight'] = 1.0
    if vasp.converged:
        return atoms
    else:
        raise ValueError(f"{directory}: VASP not converged")
def run_vasp(argparse):

    result = calculate_vasp(argparse.model_path,argparse)
    path=os.path.dirname(argparse.out_file_path)
    if path and  not os.path.exists(path):
        os.makedirs(path)

    ase_write(argparse.out_file_path,result,format="extxyz",append=argparse.append)
    print("所有计算均顺利完成！")

if __name__ == '__main__':
    calculate_vasp("./")