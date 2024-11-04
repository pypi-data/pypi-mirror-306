#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time    : 2024/11/4 11:07
# @Author  : 兵
# @email    : 1747193328@qq.com


class Test:
    def __init__(self):
        self.aaaa=1


    def a(self,v=1):
        return 1

    def aa(self,v):
        return v

    def __getattr__(self, item):
        print(item)
test=Test()
print(test.a,test.aaaaa )
print(test.aa(12) )