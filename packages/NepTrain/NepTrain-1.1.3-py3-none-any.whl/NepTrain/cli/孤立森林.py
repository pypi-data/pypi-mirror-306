#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/31 17:20
# @Author  : 兵
# @email    : 1747193328@qq.com
from sklearn.ensemble import IsolationForest
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# 示例数据：每个分子由多个原子坐标组成
molecules = [
    np.random.uniform(0, 10, (10, 3)),  # 分子1
    np.random.uniform(0, 10, (12, 3)),  # 分子2
    np.vstack([np.random.uniform(0, 10, (8, 3)), np.array([[2, 2, 2]])]),  # 分子3，其中一个原子异常
]

# 设置孤立森林模型
isolation_forest = IsolationForest(contamination=0.1, random_state=42)

# 遍历每个分子，检测每个原子的异常情况
fig = plt.figure()
for idx, molecule in enumerate(molecules):
    # 训练孤立森林模型并预测每个原子是否为异常
    isolation_forest.fit(molecule)
    labels = isolation_forest.predict(molecule)  # -1 表示异常，1 表示正常

    # 获取正常和异常原子
    normal_atoms = molecule[labels == 1]
    anomalous_atoms = molecule[labels == -1]

    # 创建子图进行3D可视化
    ax = fig.add_subplot(1, len(molecules), idx + 1, projection='3d')
    ax.scatter(normal_atoms[:, 0], normal_atoms[:, 1], normal_atoms[:, 2], c='b', label='正常原子', s=50)
    if len(anomalous_atoms) > 0:
        ax.scatter(anomalous_atoms[:, 0], anomalous_atoms[:, 1], anomalous_atoms[:, 2], c='r', label='异常原子', s=50)

    ax.set_xlabel('X 坐标')
    ax.set_ylabel('Y 坐标')
    ax.set_zlabel('Z 坐标')
    ax.set_title(f'分子 {idx + 1}')
    ax.legend()

plt.suptitle('分子原子的异常检测')
plt.show()
