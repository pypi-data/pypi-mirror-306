#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/25 18:12
# @Author  : 兵
# @email    : 1747193328@qq.com
import os.path
import shutil

from rich import get_console

from NepTrain import module_path, utils


def create_vasp(force):
    if   os.path.exists("./sub_vasp.sh") and not force:
        utils.print_tip("sub_vasp.sh已经存在，如果需要强行生成覆盖，请使用-f 或者--force。" )
        return
    sub_vasp="""#! /bin/bash
#SBATCH --job-name=NepTrain
#SBATCH --nodes=1
#SBATCH --partition=cpu
#SBATCH --ntasks-per-node=64
#这里可以放一些加载环境的命令

#例如conda activate NepTrain
#这里主要是为了直接传参
$@ 
#实际执行的脚本应该如下
#具体参数含义可以执行NepTrain vasp -h 查看
#NepTrain vasp demo.xyz -np 64 --directory ./cache -g --incar=./INCAR --kpoints 35 -o ./result/result.xyz 
"""

    with open("./sub_vasp.sh", "w",encoding="utf8") as f:
        f.write(sub_vasp)


def create_nep(force):
    if os.path.exists("./sub_gpu.sh") and not force:
        utils.print_tip("sub_gpu.sh已经存在，如果需要强行生成覆盖，请使用-f 或者--force。")
        return

    sub_vasp = """#! /bin/bash
#SBATCH --job-name=NepTrain-gpu
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --partition=gpu-a800
#SBATCH --gres=gpu:1
#这里可以放一些加载环境的命令
 
$@ """
    with open("./sub_gpu.sh", "w", encoding="utf8") as f:
        f.write(sub_vasp)

def init_template(argparse):

    if not os.path.exists("./structure"):
        os.mkdir("./structure")
        utils.print_tip("创建./structure，请将需要跑md的扩包结构放到该文件夹！" )

    create_vasp(argparse.force)
    create_nep(argparse.force)
    if not os.path.exists("./job.yaml") or argparse.force:
        shutil.copy(os.path.join(module_path,"core/train/job.yaml"),"./job.yaml")
    else:
        utils.print_tip("job.yaml已经存在，如果需要强行生成覆盖，请使用-f 或者--force。")
