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


class NepTrainWorker:
    pass


    def run(self):
        pass

    def group(self):
        pass

    def restart(self):
        if os.path.exists("./restart.json"):
            with open("./restart.json", "r",encoding="utf8") as f:
                start_info=json.load(f)


def check_current():
    pass


def train_nep():
    """
    首先检查下当前的进度 看从哪开始
    :return:
    """