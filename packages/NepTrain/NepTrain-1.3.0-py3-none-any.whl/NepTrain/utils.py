#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 16:01
# @Author  : 兵
# @email    : 1747193328@qq.com
import glob
import os
import shutil
import subprocess
import traceback
from collections import OrderedDict
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Generator, Union

import yaml
from ase.io import read as ase_read
from rich import get_console
from rich.progress import track


def ordered_yaml_load(stream, Loader=yaml.SafeLoader,
                      object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass

    def _construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))

    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        _construct_mapping)
    return yaml.load(stream, OrderedLoader)


def ordered_yaml_dump(data, stream=None, Dumper=yaml.SafeDumper,
                      object_pairs_hook=OrderedDict, **kwds):
    class OrderedDumper(Dumper):
        pass

    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())

    OrderedDumper.add_representer(object_pairs_hook, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)


def get_config_path():
    return os.path.join(os.path.expanduser('~'),".NepTrain")

def verify_path(path):
    if not os.path.exists(os.path.expanduser(path)):

        os.makedirs(os.path.expanduser(path))

def copy(rc, dst,   follow_symlinks=True):

    parent_path=(os.path.dirname(dst))
    if not os.path.exists(parent_path):
        os.makedirs(parent_path)
    shutil.copy(rc, dst,  follow_symlinks=follow_symlinks)
def copy_files(src_dir, dst_dir):
    # 遍历源目录中的所有文件
    for filename in os.listdir(src_dir):
        src_file = os.path.join(src_dir, filename)
        dst_file = os.path.join(dst_dir, filename)

        # 确保是文件而不是目录
        if os.path.isfile(src_file):
            # 复制文件
            shutil.copy2(src_file, dst_file)





def cat(files,out_file):


    # 获取所有以 'file' 开头的文件名
    if isinstance(files,str):
        file_list = glob.glob(files)
    else:
        file_list = files

    # 打开目标文件用于写入
    with open(out_file, 'wb') as outfile:
        for filename in file_list:

            with open(filename, 'rb') as infile:
                # 读取文件内容并写入到目标文件
                outfile.write(infile.read())


@contextmanager
def cd(path: Union[str, Path]) -> Generator:
    """


        with cd("/my/path/"):
            do_something()

    Args:
        path: Path to cd to.
    """
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)
def iter_path_to_atoms(glob_strs: list,show_progress=True,**kkwargs):
    def decorator(func):
        def wrapper(path: Path | str, *args, **kwargs):
            if isinstance(path, str):
                path = Path(path)
            if path.is_dir():
                parent = path
            else:
                parent = path.parent
            result =[]

            filter_path_list=[]
            for glob_str in glob_strs:
                for i in parent.glob(glob_str):

                    if path.is_file():

                        if i.name != path.name:
                            continue
                    try:
                        atoms=ase_read(i.as_posix(),index=":")
                    except Exception as e:
                        print(f"文件：{i.as_posix()}读取错误!报错原因：{e}")
                        continue
                    if isinstance(atoms,list):

                        filter_path_list.extend(atoms)
                    else:
                        filter_path_list.append(atoms)

            if show_progress:
                iter_obj=track(filter_path_list,
                              **kkwargs
                              )
            else:
                iter_obj=filter_path_list

            for i in iter_obj:

                try:
                    result.append(func(i, *args, **kwargs))
                except KeyboardInterrupt:
                    return result
                except Exception as e:
                    print(traceback.format_exc())
                    print(e)
                    pass
            return result
        return wrapper

    return decorator

def get_command_result(cmd):
    try:
        # 使用 subprocess 调用 which 命令，并捕获输出

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # 检查命令是否成功执行

        if result.returncode == 0:
            # 返回命令的路径
            return result.stdout.strip()
        else:
            # 如果命令未找到，返回 None 或抛出异常
            return None
    except Exception as e:

        return None

def is_file_empty(file_path):
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print_warning(f"文件 {file_path} 不存在。")
        return True
        # raise FileNotFoundError(f"文件 {file_path} 不存在。")

    # 检查文件大小
    return os.path.getsize(file_path) == 0
def is_diff_path(path,path1):
    return os.path.abspath(path)!=os.path.abspath(path1)

def split_list(lst, n):
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def print(*msg, **kwargs):

    get_console().print(f"[{datetime.now()}]--",*msg, **kwargs)


def print_warning(*msg):
    print(*msg, style="#fc5531")

def print_msg(*msg):
    print(*msg )

def print_tip(*msg):
    print(*msg)

def print_success(*msg):
    print(*msg, style="green")
