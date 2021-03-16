#coding=utf-8
'''
info: 本项目第一个执行的脚本，通过此脚本把apkfile下的所有apk首先通过androguard转换为gml文件存放到gml文件夹下（调用图文件）【apk2graph.extractcg（）】，然后通过【gml2txt.gml2graph（）】读取图
中的信息得到图中的节点和边，通过【gml2txt.caller2callee（）】转换为存储调用的对应.txt文件存储在txtfile文件夹下，最后一步通过【abstractGraph._preprocess_graph（）】将txt文件进行抽象，抽象出来
的文件分别存储在class、family和package文件夹下 （缺点：没考虑到效率问题，这些操作是串行运行的，能否考虑并行？）
'''

import os
import abstractGraph
import apk2graph
import gml2txt
import time

def main():
	apkfile = os.getcwd() + "/apk/"  #apk dir
	gmlfile = os.getcwd() + "/gml/"
	txtfile = os.getcwd() + "/graphs/Trial1/"
	num = 0 #num to count

	'''
	apk to gml(call graph get by androguard)
	'''

	for filename in os.listdir(apkfile):
		#print filename
		try:
			if filename.endswith(".apk"):
				gmlpath = os.getcwd() + "/gml/" + filename.rpartition(".")[0] + ".gml"
			else:
				gmlpath = os.getcwd() + "/gml/" + filename + ".gml"
			filename = apkfile + filename
			apk2graph.extractcg(filename,gmlpath)
		except:
			print filename + "to gml has some ero"
		else:
			print filename + " to gml done"

	print "<----------------------apk to gml done------------------------->"

	'''
	gml to txt(txt file that can be used by abstractGraph.py)
	'''

	for gmlname in os.listdir(gmlfile):
		try:
			storepath = txtfile + gmlname.rpartition(".")[0] + ".txt"
			gmlname = gmlfile + gmlname
			g, edgelist = gml2txt.gml2graph(gmlname)
			gml2txt.caller2callee(edgelist,g.vs,storepath)
		except:
			print gmlname + "to txt has some ero"
		else:
			print gmlname + " to txt done"
	print "<----------------------gml to txt done------------------------->"

	'''
	abstract graph
	'''
	logfile = os.getcwd()+"/log.txt"
	#print logfile
	with open(logfile,'w') as log:
		for txtname in os.listdir(txtfile):
			txtpath = txtfile + txtname
			_app_dir = os.getcwd()
			abstractGraph._preprocess_graph(txtpath,_app_dir)#txt path and pwd
			log.write(txtname.rpartition(".")[0] +".apk" + " is abstracted" + "\n")
			num+=1
		log.write(str(num) + " apks have done")
	print "<----------------------abstract done---------------	---------->"

if __name__ == "__main__":
	time_start = time.time()
	main()
	time_end = time.time()
	print "time cost:",time_end-time_start," s "