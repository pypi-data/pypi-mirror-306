#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/25 20:51
# @Author  : 兵
# @email    : 1747193328@qq.com
import re
import subprocess
import time
from threading import Thread

from NepTrain import utils


class Worker():
    pass
    def __init__(self, mode):
        self.mode = mode

        self._running=False

    @property
    def running(self):
        return self._running

    def sub_job(self,command,job_path):
        raise NotImplementedError

class LocalWorker(Worker):
    def __init__(self,  ):
        super().__init__("local")
    def sub_job(self,command,job_path):
        if self.mode == 'local':
            with utils.cd(job_path), open("job.out", "w") as f_std, open("job.err", "w", buffering=1) as f_err:
                self._running=True
                subprocess.check_call(command, stdout=f_std, stderr=f_err )
                self._running=False

class SlurmWorker(Worker):
    def __init__(self,  ):
        super().__init__("slurm")
        #创建一个线程  定时检查任务状态？
        self.job_id=None
        self._thread=Thread(target=self.check_job_state)
        self._thread.start()
    def sub_job(self,command,job_path):
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        self.job_id=int(result.stdout.replace("Submitted batch job ",""))
        print("提交任务",self.job_id)

    def check_job_state(self):
        while True:
            result = subprocess.run(['squeue','-j',f"{self.job_id}"], capture_output=True, text=True, check=True)
            match = re.search(r'JOBID.*?(\d+) ', result.stdout, re.S)
            #
            # 如果找到匹配项，打印作业ID
            if match:
                # job_id = match.group(1)
                self._running=True
                time.sleep(5)

            else:
                self._running=False
                break