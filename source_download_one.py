#!/usr/bin/env python

import subprocess
import os
import hash_lib
import graph
import strace

pkgName = input("Please enter package name to build a package from source: ")
path = './temp/' + pkgName + '/'

cmd = 'rm -rf ' + path
logs = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
cmd = ['mkdir', path]
logs = subprocess.run(cmd, stdout=subprocess.PIPE)

os.chdir(path)

graph = graph.getInstance() # call graph singleton instance

cmd = 'sudo apt-get source ' + pkgName
graph.add_vertex(cmd)
logs = subprocess.call(cmd, shell=True)

# log the output of 'apt-get source' command to graph object
for root, dirs, files in os.walk('./'): 
   for filename in files:
        checksum = hash_lib.sha256sum(os.path.join(root, filename))
        graph.add_edge(cmd, checksum, filename) # add edge connecting 'apt-get source' command to output file

cmd = 'sudo apt-get build-dep -y ' + pkgName
graph.add_vertex(cmd)
logs = subprocess.call(cmd, shell=True)

# log the output of 'apt-get build-dep' command to graph object
logs = subprocess.check_output('apt-cache showsrc ' + pkgName + ' | grep -oP "(?<=Build-Depends:).*"', universal_newlines=True, shell=True) # list packages needed to build from source
deps = logs.split(',')
for dep in deps:
       dep_name = dep.split('(')[0] # ignore version of the dependency
       logs = subprocess.check_output('dpkg -L ' + dep_name, universal_newlines=True, shell=True) # list the files installed
       paths = logs.split('\n')
       for path in paths:     
               isFile = os.path.isfile(path)
               if isFile:
                        checksum = hash_lib.sha256sum(path)
                        graph.add_edge(cmd, checksum, path) # add edge connecting 'apt-get build-dep' command to output file

count = 0
for x in os.listdir('./'):
    if os.path.isdir(x):
        os.chdir(x)
        strace.straceExe('dpkg-buildpackage -us -uc -b', x)
        os.chdir('../')
        count += 1

if count == 0:
    print(path + ' にはディレクトリないかも？')

os.chdir('../../')