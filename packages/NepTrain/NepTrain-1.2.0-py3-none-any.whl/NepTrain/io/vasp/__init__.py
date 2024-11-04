#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/25 19:10
# @Author  : 兵
# @email    : 1747193328@qq.com
from NepTrain import Config

from ase.calculators.vasp.setups import setups_defaults
from .inputs import VaspInput
for option in Config.options("potcar"):
    v=Config.get("potcar", option).replace(option, "")

    setups_defaults["recommended"][option.title()]=v


