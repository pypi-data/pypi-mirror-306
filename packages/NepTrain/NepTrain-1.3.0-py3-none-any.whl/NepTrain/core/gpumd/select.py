#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/29 19:52
# @Author  : 兵
# @email    : 1747193328@qq.com
import os

import numpy as np
from ase.io import read as ase_read
from calorine.nep import get_descriptors
from matplotlib import pyplot as plt
from scipy.spatial.distance import cdist
from sklearn.decomposition import PCA


# 从pynep复制的最远点采样 就使用这一个函数 因为安装不方便
def select(new_data, now_data=[], min_distance=None, min_select=1, max_select=None):
    """Select those data fartheset from given data

    Args:
        new_data (2d list or array): A series of points to be selected
        now_data (2d list or array): Points already in the dataset.
            Defaults to []. (No existed data)
        min_distance (float, optional):
            If distance between two points exceeded the minimum distance, stop the selection.
            Defaults to None (use the self.min_distance)
        min_select (int, optional): Minimal numbers of points to be selected. This may cause
            some distance between points less than given min_distance.
            Defaults to 1.
        max_select (int, optional): Maximum numbers of points to be selected.
            Defaults to None. (No limitation)

    Returns:
        A list of int: index of selected points
    """
    metric = 'euclidean'
    metric_para = {}
    min_distance = min_distance
    max_select = max_select or len(new_data)
    to_add = []
    if len(new_data) == 0:
        return to_add
    if len(now_data) == 0:
        to_add.append(0)
        now_data.append(new_data[0])
    distances = np.min(cdist(new_data, now_data, metric=metric, **metric_para), axis=1)

    while np.max(distances) > min_distance or len(to_add) < min_select:
        i = np.argmax(distances)
        to_add.append(i)
        if len(to_add) >= max_select:
            break
        distances = np.minimum(distances, cdist([new_data[i]], new_data, metric=metric)[0])
    return to_add




def select_structures(train, new ,nep_path, max_selected=20, min_distance=0.01):
    # 首先去掉跑崩溃的结构

    new_atoms = ase_read(new, ":", format="extxyz", do_not_split_by_at_sign=True)

    # new_atoms = remove_garbage_structure(new_atoms)

    train_des = np.array([np.mean(get_descriptors(i, nep_path), axis=0) for i in train])

    new_des = np.array([np.mean(get_descriptors(i, nep_path), axis=0) for i in new_atoms])

    selected_i = select(np.vstack([train_des, new_des]), train_des, min_distance=min_distance, max_select=max_selected,
                        min_select=0)
    # 画一下图

    reducer = PCA(n_components=2)
    reducer.fit(np.vstack([train_des, new_des]))
    fig = plt.figure()

    proj = reducer.transform(train_des)
    plt.scatter(proj[:, 0], proj[:, 1], label='train', c="gray")

    proj = reducer.transform(new_des)
    plt.scatter(proj[:, 0], proj[:, 1], label='MD dataset', c="#07cd66")


    if selected_i:
        selected_proj = reducer.transform(np.array([new_des[i - train_des.shape[0]] for i in selected_i]))
        plt.scatter(selected_proj[:, 0], selected_proj[:, 1], label='selected', c="red")
    plt.legend()
    plt.axis('off')

    plt.savefig(os.path.join(os.path.dirname(new), "select.png"))
    plt.close(fig)

    return [new_atoms[i - train_des.shape[0]] for i in selected_i]

