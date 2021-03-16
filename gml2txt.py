#coding=utf-8
import sys
import os
import igraph
import parse
from collections import defaultdict



gmlpath="./apk/百度翻译.gml"

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
    

