#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/25 13:37
# @Author  : 兵
# @email    : 1747193328@qq.com
"""
自动训练的逻辑
"""
import json
import os.path
import logging
from .worker import LocalWorker,SlurmWorker
import yaml
from ase.io import read as ase_read
from ase.io import write as ase_write
from NepTrain import utils,Config
from ..utils import check_env
import shutil
class Manager:
    def __init__(self, options):
        self.options = options
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.options):
            self.index = 0
        value = self.options[self.index]
        self.index += 1
        return value

    def set_next(self, option):
        index=self.options.index(option)
        # 设置当前索引，注意索引从0开始
        if 0 <= index < len(self.options):
            self.index = index
        else:
            raise IndexError("Index out of range.")



class NepTrainWorker:
    pass
    def __init__(self):
        self.config={}
        self.manager=Manager(["vasp","nep","gpumd" ])

    def run(self):
        pass

    def group(self):
        pass

    @property
    def vasp_work_path(self):
        path=os.path.join(self.generation_path,"vasp")
        utils.verify_path(path)
        return path


    @property
    def gpumd_work_path(self):
        path=os.path.join(self.generation_path,"gpumd")
        utils.verify_path(path)
        return path
    @property
    def nep_work_path(self):
        path=os.path.join(self.generation_path,"nep")
        utils.verify_path(path)
        return path

    @property
    def last_generation_path(self):
        path=os.path.join(os.path.abspath(self.config.get("work_path")), f"Generation-{self.generation-1}")
        utils.verify_path(path)

        return path

    @property
    def generation_path(self):
        path=os.path.join(os.path.abspath(self.config.get("work_path")), f"Generation-{self.generation}")
        utils.verify_path(path)
        return path

    @property
    def generation(self):
        return self.config.get("generation")
    @generation.setter
    def generation(self,value):
        self.config["generation"] = value



    def check_env(self):


        if self.generation!=1 or self.config.get("restart") :
            print("无需初始化检查")
            return

        if self.config["current_job"]=="vasp":

            self.generation=0

            if self.config["vasp_job"] != 1:
                shutil.copy(self.config["init_train_xyz"], os.path.join(self.generation_path, "learn-add.xyz"))

                addxyz = ase_read(self.config["init_train_xyz"], ":", format="extxyz")

                split_addxyz_list = utils.split_list(addxyz, self.config["vasp_job"])

                for i, xyz in enumerate(split_addxyz_list):
                    ase_write(os.path.join(self.gpumd_work_path, f"./learn-add-{i + 1}.xyz"), xyz, format="extxyz")
            else:
                shutil.copy(self.config["init_train_xyz"], os.path.join(self.generation_path, "learn-add.xyz"))
        elif self.config["current_job"]=="nep":
            shutil.copy(self.config["init_train_xyz"], os.path.join(self.last_generation_path, "all-learn-calculated.xyz"))
            #如果势函数有效  直接先复制过来
        elif self.config["current_job"]=="gpumd":

            shutil.copy(self.config["init_train_xyz"], os.path.join(self.nep_work_path, "train.xyz"))

            if os.path.exists(self.config["init_nep_txt"]):
                shutil.copy(self.config["init_nep_txt"],
                            os.path.join(self.nep_work_path, "nep.txt"))
            else:
                raise FileNotFoundError("开始任务为gpumd必须指定有效的势函数路径！")
        else:
            raise ValueError("current_job 只能是nep,gpumd,vasp其中一个")

    def read_config(self,config_path):
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"{config_path}文件不存在")
        with open(config_path,"r",encoding="utf8") as f:
            # self.config=json.load(f)

            self.config=yaml.load(f,Loader=yaml.FullLoader)




    def build_nep_params(self  ):
        nep=self.config["nep"]
        params=[]
        params.append("NepTrain")
        params.append("nep")

        params.append("--directory")
        params.append(os.path.join(self.generation_path,f"nep"))

        params.append("--in")
        params.append(os.path.abspath(nep.get("nep_in_path")))

        params.append("--train")
        params.append(os.path.join(self.last_generation_path, f"improved_train.xyz"))

        params.append("--test")
        params.append(os.path.abspath(nep.get("test_xyz_path")))


        if self.config["nep"]["nep_restart"]:
            #开启续跑
            #如果上一级的势函数路径有效  就传入一下续跑的参数
            if os.path.exists(os.path.join(self.last_generation_path,"nep/nep.restart")):
                params.append("--restart_file")
                params.append(os.path.join(self.last_generation_path,"nep/nep.restart"))
                params.append("--continue_step")
                params.append(str(self.config["nep"]["nep_restart_step"]))

        return " ".join(params)
    def build_gpumd_params(self,n_job=1):
        gpumd=self.config["gpumd"]
        params=[]
        params.append("NepTrain")
        params.append("gpumd")

        params.append(os.path.abspath(gpumd.get("model_path")))

        params.append("--directory")

        params.append(self.gpumd_work_path)

        params.append("--in")
        params.append(os.path.abspath(gpumd.get("run_in_path")))
        params.append("--nep")
        params.append( os.path.join(self.nep_work_path, "nep.txt"))
        params.append("--time")
        params.append(str(gpumd.get("step_times")[self.generation-1]))

        params.append("--temperature")

        params.append(" ".join([str(i) for i in gpumd["temperature_every_step"]]))


        params.append("--train")
        params.append( os.path.join(self.nep_work_path, f"train.xyz"))
        params.append("--max_selected")
        params.append(str(gpumd["max_selected"]))
        params.append("--min_distance")
        params.append(str(gpumd["min_distance"]))
        params.append("--out")
        params.append(os.path.join(self.gpumd_work_path,f"learn-{n_job}.xyz"))



        return " ".join(params)

    def build_vasp_params(self,n_job=1):
        vasp=self.config["vasp"]
        params=[]
        params.append("NepTrain")
        params.append("vasp")

        if self.config["vasp_job"] == 1:

            params.append(os.path.join(self.gpumd_work_path,"learn-add.xyz"))
        else:
            params.append(os.path.join(self.gpumd_work_path,f"learn-add-{n_job}.xyz"))

        params.append("--directory")
        params.append(os.path.join(self.generation_path,f"vasp/cache{n_job}"))

        params.append("-np")
        params.append(str(vasp["cpu_core"]))
        if vasp["kpoints_use_gamma"]:
            params.append("--gamma")

        if vasp["incar_path"]:

            params.append("--incar")
            params.append(os.path.abspath(vasp["incar_path"]))
        if vasp["use_k_stype"]=="kpoints":
            if vasp.get("kpoints"):
                params.append("--kpoints")
                if isinstance(vasp["kpoints"],list):
                    params.append(",".join([str(i) for i in vasp["kpoints"]]))
                else:
                    params.append(str(vasp["kpoints"]))
        else:

            if vasp.get("kspacing") :
                params.append("--kspacing")
                params.append(str(vasp["kspacing"]))
        params.append("--out")

        params.append(os.path.join(self.vasp_work_path,f"learn-calculated-{n_job}.xyz"))

        return " ".join(params)



    def sub_vasp(self):
        utils.print_msg("开始执行VASP计算单点能")
        if not utils.is_file_empty(os.path.join(self.generation_path, "learn-add.xyz")):
            for i in range(self.config["vasp_job"]):
                cmd = self.build_vasp_params(i + 1)

                self.worker.sub_job(cmd, self.vasp_work_path, job_type="vasp")

            self.worker.wait()
            utils.cat(os.path.join(self.vasp_work_path, f"learn-calculated-*.xyz"),
                      os.path.join(self.generation_path, f"all-learn-calculated.xyz")
                      )
        else:
            utils.print_warning("检测到计算输入文件为空，直接进入下一步！")

            utils.cat(os.path.join(self.generation_path, "learn-add.xyz"),
                      os.path.join(self.generation_path, f"all-learn-calculated.xyz")
                      )
        self.generation += 1

    def sub_nep(self):
        utils.print_msg("--" * 10, f"开始训练第{self.generation}代势函数", "--" * 10)

        if not utils.is_file_empty(os.path.join(self.last_generation_path, f"all-learn-calculated.xyz")):


            if os.path.exists(os.path.join(self.last_generation_path, f"nep/train.xyz")):
                utils.cat([os.path.join(self.last_generation_path, f"nep/train.xyz"),
                           os.path.join(self.last_generation_path, f"all-learn-calculated.xyz")
                           ],
                          os.path.join(self.last_generation_path, f"improved_train.xyz")
                          )
            else:
                shutil.copy(os.path.join(self.last_generation_path, f"all-learn-calculated.xyz"),
                            os.path.join(self.last_generation_path, f"improved_train.xyz"))
            utils.print_msg(f"开始训练势函数")
            cmd = self.build_nep_params()
            self.worker.sub_job(cmd, self.nep_work_path, job_type="nep")
            self.worker.wait()
        else:
            utils.print_warning("数据集没有变化，直接复制上一次的势函数！")
            if os.path.exists(os.path.join(self.generation_path,"nep")):
                shutil.rmtree(os.path.join(self.generation_path,"nep"))
            shutil.copytree(os.path.join(self.last_generation_path,"nep"), os.path.join(self.generation_path,"nep"))
    def sub_gpumd(self):
        utils.print_msg(f"开始主动学习")

        cmd = self.build_gpumd_params()

        self.worker.sub_job(cmd, self.gpumd_work_path, job_type="gpumd")
        self.worker.wait()
        utils.cat(os.path.join(self.gpumd_work_path, f"learn-*.xyz"),
                  os.path.join(self.generation_path, f"learn-add.xyz")
                  )

        if utils.is_file_empty(os.path.join(self.generation_path, f"learn-add.xyz")):
            # 文件为空

            utils.print_warning("本轮主动学习添加结构为0！")

            return

        # break
        if self.config["vasp_job"] != 1:
            # 这里分割下xyz 方便后面直接vasp计算
            addxyz = ase_read(os.path.join(self.generation_path, f"learn-add.xyz"), ":", format="extxyz")

            split_addxyz_list = utils.split_list(addxyz, self.config["vasp_job"])

            for i, xyz in enumerate(split_addxyz_list):
                ase_write(os.path.join(self.generation_path, f"learn-add-{i + 1}.xyz"), xyz, format="extxyz")

    def start(self,config_path):
        utils.print_msg("欢迎使用NepTrain自动训练！")

        self.read_config(config_path)
        self.check_env()
        #首先创建一个总的路径
        #然后先

        if self.config.get("queue")=="local":
            self.worker=LocalWorker( )
        else:
            self.worker=SlurmWorker(os.path.abspath("./sub_vasp.sh"),os.path.abspath("./sub_gpu.sh") )
        self.manager.set_next(self.config.get("current_job"))

        while True:

            #开始循环
            job=next(self.manager)
            self.config["current_job"]=job
            self.save_restart()
            if job=="vasp":

                self.sub_vasp()

            elif job=="nep":

               self.sub_nep()
            else:
                self.sub_gpumd()


    def save_restart(self):
        with open("./restart.yaml","w",encoding="utf-8") as f:
            self.config["restart"]=True

            yaml.dump(self.config,f)

def train_nep(argparse):
    """
    首先检查下当前的进度 看从哪开始
    :return:
    """
    check_env()

    worker = NepTrainWorker()
    # worker.start("..//core/train/job.json")
    worker.start(argparse.config_path)
