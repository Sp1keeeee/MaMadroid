#coding=utf-8
'''
info：gml2graph函数通过读取gml文件得到调用图中的所有节点以及边信息，caller2callee通过调用parse.py中的方法将gml文件中的调用图信息转换为txt文件
'''
import sys
import os
import igraph
import parse
from collections import defaultdict



gmlpath="./apk/file1.gml"

reload(sys)
sys.setdefaultencoding('utf8')


def caller2callee(edgelist,nodes,filename):#edgelist:all edges   nodes:all nodes filename:file to store
    #print edgelist
    edges = defaultdict(list)
    edgesname =  defaultdict(list)
    for k,v in edgelist:
        edges[k].append(v)
    #print edges
    for k,v in edgelist:
        edgesname[parse.parse_label(nodes[k]["label"])].append(parse.parse_label(nodes[v]["label"]) + "\n")
    with open(filename, 'w') as out:
        for node in edgesname:
            call = str(node) + " ==> " + str(edgesname[node])
            out.write(call + "\n")

def gml2graph(gmlpath):
    g = igraph.Graph.Read_GML(gmlpath)
    '''
        for node in g.vs:
            print node
            print node["label"]
        '''
    edgelist = g.get_edgelist()
    return g, edgelist

if __name__ == '__main__':
    #extractcg()
    g, edgelist = gml2graph(gmlpath)


    apifile = "/data/zhangchennan/mamatest/callgraph2.txt"
    caller2callee(edgelist,g.vs,apifile)
    

