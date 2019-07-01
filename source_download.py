#!/usr/bin/env python

import subprocess
import os
import hash_lib

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

graph = graph.Graph.getInstance() # call graph singleton instance

for i in fList:
    # print(i)
    cmd = ['mkdir', './temp/' + i]
    # print(cmd)
    logs = subprocess.run(cmd, stdout=subprocess.PIPE)

    os.chdir('./temp/' + i)

    cmd = 'sudo apt-get source ' + i
    hash_cmd = hash_lib.sha256string(cmd)
    graph.add_vertex(hash_cmd)
    logs = subprocess.call(cmd, shell=True)

    # log the output of 'apt-get source' command to graph instance
    for root, dirs, files in os.walk('./temp/' + i): 
      for filename in files:
           checksum = hash_lib.sha256sum(filename)
           graph.add_edge(hash_cmd, checksum, filename) # add edge connecting 'apt-get source' command to output file

    cmd = 'sudo apt-get build-dep -y ' + i
    hash_cmd = hash_lib.sha256string(cmd)
    graph.add_vertex(hash_cmd)
    logs = subprocess.call(cmd, shell=True)

    # log the output of 'apt-get build-dep' command to graph instance
    logs = subprocess.check_output('apt-cache showsrc ' + i + ' | grep -oP "(?<=Build-Depends:).*"', universal_newlines=True, shell=True) # list packages needed to build from source
    deps = logs.split(',')
    for dep in deps:
           dep_name = dep.split('(')[0] # ignore version of the dependency
           logs = subprocess.check_output('dpkg -L ' + dep_name, universal_newlines=True, shell=True) # list the files installed
           paths = logs.split('\n')
           for path in paths:     
                   isFile = os.path.isfile(path)
                   if isFile:
                            checksum = hash_lib.sha256sum(path)
                            graph.add_edge(hash_cmd, checksum, path) # add edge connecting 'apt-get build-dep' command to output file

    # for v in graph:
    # 	for w in v.get_connections():
    # 		vid = v.get_id()
    # 		wid = w.get_id()
    # 		print (vid, wid)
    
    os.chdir('../../')
