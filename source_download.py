#!/usr/bin/env python

import subprocess
import os
import pexpect

# このファイルとファイルリストが同じ階層に置かれていることが前提
listPath = './sourceList.txt'
fList = []

cmd = 'rm -rf ./temp/'
logs = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
cmd = ['mkdir', './temp']
logs = subprocess.run(cmd, stdout=subprocess.PIPE)

with open(listPath) as f:
    for x in f:
        # print(x)
        fList.append(x.rstrip("\n"))

# print(fList)

for i in fList:
    # print(i)
    cmd = ['mkdir', './temp/' + i]
    # print(cmd)
    logs = subprocess.run(cmd, stdout=subprocess.PIPE)

    os.chdir('./temp/' + i)

    cmd = ['sudo', 'apt-get', 'source', i]
    logs = subprocess.call(cmd)
    cmd = ['sudo', 'apt-get', 'build-dep', '-y', i]
    logs = subprocess.call(cmd)

    os.chdir('../../')
