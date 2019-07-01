#!/usr/bin/env python
import os
import strace

pkgName = input("Please Enter build package name in temp dir : ")
path = './temp/' + pkgName + '/'

count = 0
for x in os.listdir(path):
    if os.path.isdir(path + x):
        os.chdir(path + x)
        strace.straceExe('dpkg-buildpackage -us -uc -b', x)
        os.chdir('../../..')
        count += 1

if count == 0:
    print(path + ' にはディレクトリないかも？')
