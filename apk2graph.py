# coding:utf-8
'''
info:通过使用androguard把目标为apkpath的APK转换为API调用图存储在路径为gmlpath的gml文件中
'''
import sys
import os

from collections import defaultdict




reload(sys)
sys.setdefaultencoding('utf8')
def extractcg(apkpath,gmlpath):

    cmd="/data/zhangchennan/anaconda3/envs/py2/bin/androguard cg {} -o {}".format(apkpath,gmlpath)
    os.system(cmd)
    print "success"


if __name__ == '__main__':
    apkpath = "./apk/VirusShare_0a1a6dc44b78e5e59a186536e652bf63"
    gmlpath = "./apk/VirusShare_0a1a6dc44b78e5e59a186536e652bf63.gml"
    extractcg(apkpath,gmlpath)
    
