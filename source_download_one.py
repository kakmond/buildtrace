#!/usr/bin/env python

import subprocess
import os
import hash_lib
import graph

pkgName = input("Please enter package name to build a package from source: ")
path = './temp/' + pkgName + '/'

cmd = 'rm -rf ' + path
logs = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)
cmd = ['mkdir', path]
logs = subprocess.run(cmd, stdout=subprocess.PIPE)

os.chdir(path)

graph = graph.Graph() # initialize the graph object

cmd = 'sudo apt-get source ' + pkgName
hash_cmd = hash_lib.sha256string(cmd)
graph.add_vertex(hash_cmd)
logs = subprocess.call(cmd, shell=True)

# log the output of 'apt-get source' command to graph object
for root, dirs, files in os.walk(path): 
   for filename in files:
        checksum = hash_lib.sha256sum(filename)
        graph.add_edge(hash_cmd, checksum, filename) # add edge connecting 'apt-get source' command to output file

cmd = 'sudo apt-get build-dep -y ' + pkgName
hash_cmd = hash_lib.sha256string(cmd)
graph.add_vertex(hash_cmd)
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
                        graph.add_edge(hash_cmd, checksum, path) # add edge connecting 'apt-get build-dep' command to output file
os.chdir('../../')

# create /buildtrace/{packageName}/graph folder
working_dir = './temp/' + pkgName + '/'
for x in os.listdir(working_dir):
    if os.path.isdir(working_dir + x):
        cmd = ['mkdir', '-p', '/buildTrace/' + x + '/graph'] 
        logs = subprocess.run(cmd, stdout=subprocess.PIPE)
        # write the graph data structure to file
        for node in graph:
                for edge in node.get_connections():
                    with open('/buildTrace/' + x + '/graph/graph_all.txt', 'a') as graph_file:
                        graph_file.write(node.get_id() + ' : ' + edge.get_id() + '\n')
        break