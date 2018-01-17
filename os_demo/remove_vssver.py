#!/usr/bin/env python
# -*- coding: gbk -*-

# 删除vssver.scc文件，这个文件是过时的版本管理方式，现在已经不用了


import os

current_dir = os.getcwd()

print current_dir

for root, dirs, files in os.walk(current_dir):
    for name in files:
        #print os.path.join(root, name)
        if name == 'vssver.scc':
            #print name
            #print os.path.join(root, name), os.path.exists(os.path.join(root, name))
            os.remove(os.path.join(root, name))

