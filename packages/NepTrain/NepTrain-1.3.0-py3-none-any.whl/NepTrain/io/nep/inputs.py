#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 15:42
# @Author  : 兵
# @email    : 1747193328@qq.com
import os
import re
import shutil
import subprocess
import sys


# sys.path.append('../../../')



from NepTrain.io.utils import NepFileMoniter


from ase.data import chemical_symbols, atomic_numbers
from NepTrain import utils, Config, observer


class RunInput:

    def __init__(self,train_xyz_path,nep_in_path=None,test_xyz_path=None):
        self.nep_in_path = nep_in_path
        self.train_xyz_path = train_xyz_path
        self.test_xyz_path = test_xyz_path
        self.run_in={"generation":100000}



        if self.nep_in_path is not None and os.path.exists(self.nep_in_path):
            self.read_run(self.nep_in_path)
        self.command=Config.get('environ','nep_path')

    def read_run(self,file_name):
        with open(file_name,'r',encoding="utf8") as f:
            groups=re.findall("(\w+)\s+(.*?)\n",f.read()+"\n")

            for group in groups:
                self.run_in[group[0]]=group[1]

    def build_run(self):
        """
        如果runin 不存在 就遍历训练集  然后找出所有的元素

        :return:
        """
        if os.path.exists(self.train_xyz_path):
            with open(self.train_xyz_path,'r',encoding="utf8") as f:
                trainxyz=f.read()
            groups=re.findall("^([A-Z][a-z]?)\s+",trainxyz,  re.MULTILINE)
            groups=set(groups)
            symbols=[]
            for symbol in groups:
                if symbol in chemical_symbols:
                    symbols.append(symbol)

            symbols = sorted(symbols,key=lambda x:atomic_numbers[x])

            self.run_in["type"]=f"{len(symbols)} {' '.join(symbols)}"

    def write_run(self,file_name):
        if  "type" not in   self.run_in :
            self.build_run()
        with open(file_name,'w',encoding="utf8") as f:
            for k,v in self.run_in.items():

                f.write(f"{k}     {v}\n" )


    def calculate(self,directory,show_progress=True):
        if not os.path.exists(directory):
            os.makedirs(directory )

        self.write_run(os.path.join(directory,"nep.in"))
        if self.train_xyz_path is   None or not  os.path.exists(self.train_xyz_path):
            raise ValueError("必须指定一个有效的train.xyz")
        if utils.is_diff_path(self.train_xyz_path ,os.path.join(directory,"train.xyz")):

            shutil.copy(self.train_xyz_path,os.path.join(directory,"train.xyz"))
        if self.test_xyz_path is not None and os.path.exists(self.test_xyz_path):
            shutil.copy(self.test_xyz_path, os.path.join(directory, "test.xyz"))
        if show_progress:

            handler=NepFileMoniter(os.path.join(directory,"loss.out"),self.run_in["generation"])
            watch=observer.schedule(handler, os.path.abspath(directory) , recursive=False)


            if not observer.is_alive():

                observer.start()

        with   open(os.path.join(directory,"nep.out"), "w") as f_std, open(os.path.join(directory,"nep.err"), "w", buffering=1) as f_err:

            errorcode = subprocess.call(self.command,
                                        shell=True,
                                        stdout=f_std,
                                        stderr=f_err,
                                        cwd=directory)


        if show_progress:

            handler.finish()
            observer.unschedule(watch)
            observer.stop()

class PredictionRunInput(RunInput):
    def __init__(self,nep_txt_path,*args,**kwargs):
        self.nep_txt_path=nep_txt_path
        super().__init__(*args,**kwargs)

    def write_run(self,file_name):

        self.run_in["prediction"]=1
        super().write_run(file_name)

    def calculate(self,directory,show_progress=False ):
        if self.nep_txt_path is not None and os.path.exists(self.nep_txt_path):
            if utils.is_diff_path(self.nep_txt_path, os.path.join(directory, "nep.txt")):

                shutil.copy(self.nep_txt_path, os.path.join(directory, "nep.txt"))
        else:
            raise ValueError("预测模式必须指定一个势函数，请通过--nep nep_path指定。")
        super().calculate(directory,show_progress)
if __name__ == '__main__':
    run=RunInput("./train1.xyz")
    # run.read_run("./nep.in")
    run.write_run("./nep.out")
    run.calculate("./")