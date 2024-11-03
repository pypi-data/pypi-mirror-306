#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/28 17:34
# @Author  : 兵
# @email    : 1747193328@qq.com
import os
import time
import traceback
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from NepTrain import utils
from tqdm import tqdm

class NepFileMoniter(FileSystemEventHandler):
    def __init__(self,file_path,total):

        self.file_path = file_path
        self.pbar=tqdm(total=int(total),desc="NEP训练中")
    def on_modified(self, event):

        if not utils.is_diff_path(event.src_path , self.file_path):
            with open(self.file_path,'r',encoding="utf8") as f:
                lines = f.readlines()
                if not lines:
                    return
                last_line=lines[-1]
                current_steps=int(last_line.split(" ")[0])
                self.pbar.n = current_steps
                self.pbar.refresh()

    def finish(self):

        if self.pbar.n!=self.pbar.total:
            self.pbar.n=self.pbar.total
            self.pbar.refresh()

        self.pbar.close()






