#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/28 15:01
# @Author  : 兵
# @email    : 1747193328@qq.com
import os

from NepTrain.io.nep.inputs import RunInput,PredictionRunInput
from NepTrain.plot import plot_nep_result

def run_nep(argparse):



    if argparse.prediction:



        run = PredictionRunInput(argparse.nep_txt_path,argparse.train_path,argparse.nep_in_path,argparse.test_path)
    else:

        run = RunInput(argparse.train_path,argparse.nep_in_path,argparse.test_path)



    run.calculate(argparse.directory)
    plot_nep_result(argparse.directory)
    print("所有计算均顺利完成！")