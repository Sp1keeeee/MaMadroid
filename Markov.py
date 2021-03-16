#coding=utf-8
'''
info:读取不同模式得到的抽象后的txt文件转换为马尔可夫矩阵
'''
import numpy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


#Dummy Coding for Markov Transition matrix
def dummycoding (imported,allnodes,wf):#imported：每一行为一个抽象后的调用信息 #allnodes:所有可能的状态 wf：标志位


	DCVector=[]
	DNSCounter=0
	for i in range (0,len(imported)): #对每一行的调用信息 放入这一行对应的DCvector[i]中
	
		DCVector.append([]) #有一个调用信息就增加一个数组
		if wf=='Y':
			callsline=imported[i].split('\t')
			#print "callsline: ",callsline
		else:
			callsline=imported[i]
		for v in range (0,len(callsline)):	#把存在的family或者package放入DCvector中
			for s in range (0,len(allnodes)):

			        if (callsline[v]==allnodes[s]):
        			        DCVector[i].append(s)

        return DCVector

# This function creates the output matrix that is showing all the transitions probabilities from one state to the other.
def matrixcreation (DCVector,allnodes):#对于每个作为caller的api 计算它对其他api调用的概率 （每个caller下的所有状态传递总和为1）
	s=(len(allnodes),len(allnodes))
	MarkovTransition= numpy.zeros(s)
	MarkovFeats= numpy.zeros(s)

	for s in range (0,len(DCVector)):
		for i in range (1,len(DCVector[s])):
		        MarkovTransition [DCVector[s][0],DCVector[s][i]]=MarkovTransition [DCVector[s][0],DCVector[s][i]]+1#有相应的调用 对应的地方置为1
    
	for i in range (0, len(MarkovTransition)):
	        Norma= numpy.sum (MarkovTransition[i])
	        if (Norma==0):
		        MarkovFeats[i]=MarkovTransition[i]
	        
	       	else:
	       		MarkovFeats[i]= MarkovTransition[i]/Norma #将结果变为小数即概率
        
    
	return MarkovFeats  

       
def main (imported,alln,wf):
    
	(DCV)= dummycoding (imported,alln,wf)
	MarkovFeatures= matrixcreation(DCV,alln)
	return MarkovFeatures
