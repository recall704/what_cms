#!/usr/bin/env python
#coding:utf-8

import os


cwd = os.getcwd()
file_list = []

for root,dirs,files in os.walk(cwd):
    for fn in files:
        if fn == "GetFileList.py":
            pass
        else:
            file_list.append(root + os.sep + fn)
        
f = open("dir.txt","w")
for fn in file_list:
    f.write("/".join(fn[len(cwd):].split(os.sep)))
    f.write(os.linesep)
f.close