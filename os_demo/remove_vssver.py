#!/usr/bin/env python
# -*- coding: gbk -*-

# ɾ��vssver.scc�ļ�������ļ��ǹ�ʱ�İ汾����ʽ�������Ѿ�������


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

