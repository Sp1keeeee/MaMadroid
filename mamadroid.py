#coding=utf-8
'''
info: This is the first script to run after succesfully compiling the Appgraph.java file. 
It uses soot to generate the callgraph and parses the graph and abstract the API calls for use by the MaMaStat.py script. 
It accepts two arguments using the -f (or --file ) and -d (or --dir) options which specifies respectively, the APK file 
(or directory with APK files) to analyze and the to your Android platform directory. Use the -h option to view the help message. 
You can also edit the amount of memory allocated to the JVM heap space to fit your machine capabilities.
'''

import os
import abstractGraph
import apk2graph
import gml2txt
import time

def main():
	apkfile = os.getcwd() + "/apk/"
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