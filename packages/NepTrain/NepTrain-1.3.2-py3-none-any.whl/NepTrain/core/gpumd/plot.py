#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/29 19:56
# @Author  : 兵
# @email    : 1747193328@qq.com
import os.path

import numpy as np
from calorine.gpumd import read_thermo
from calorine.nep import get_descriptors
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA


def plot_all_structure(train_data, add_data,nep_path, save_path):
    train_des = np.array([np.mean(get_descriptors(i, nep_path), axis=0) for i in train_data])
    add_des = np.array([np.mean(get_descriptors(i, nep_path), axis=0) for i in add_data])

    reducer = PCA(n_components=2)
    reducer.fit(np.vstack([train_des, add_des]))

    fig = plt.figure()

    proj = reducer.transform(train_des)
    plt.scatter(proj[:, 0], proj[:, 1], label='train', c="gray")

    proj = reducer.transform(add_des)
    plt.scatter(proj[:, 0], proj[:, 1], label='add', c="#07cd66")

    plt.legend()
    plt.axis('off')

    plt.savefig(save_path)
    plt.close(fig)


def plot_energy(thermo_path,natoms=1):
    data = read_thermo(thermo_path, natoms)

    potential_energy = data.potential_energy.to_numpy(dtype='float')

    fig = plt.figure()
    plt.plot(list(range(potential_energy.shape[0])), potential_energy)



    plt.savefig(os.path.join(os.path.dirname(thermo_path),"md_energy.png"), dpi=300)