#!/usr/bin/env python

import subprocess
import os
import glob
import strace

# このファイルとファイルリストが同じ階層に置かれていることが前提
listPath = './sourceList.txt'
fList = []

with open(listPath) as f:
    for x in f:
        # print(x)
        fList.append('./temp/' + x.rstrip("\n") + '/')

# print(fList)

for path in fList:
    count = 0
    for x in os.listdir(path):
        if os.path.isdir(path + x):
            os.chdir(path + x)
            strace.straceExe('dpkg-buildpackage -us -uc -b', x)
            os.chdir('../../..')
            count += 1

    if count == 0:
        print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')
        print(path + ' にはディレクトリないかも？')
        print('wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww')