#coding=utf-8
'''
info：通过Families11.txt文件作为名单调用Markov.py把family文件夹下的文件转换为马尔可夫矩阵存放到Features/Families文件夹下
'''
import numpy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import Markov as mk
import os
from time import time
import numpy as np

PACKETS = []

WHICHCLASS = "Families"

wf = "Y"
appslist = None
dbs = None

with open("Families11" + '.txt') as packseq:
    for line in packseq:
        PACKETS.append(line.replace('\n', ''))
packseq.close()
allnodes = PACKETS
allnodes.append('self-defined')
allnodes.append('obfuscated')
print "allnoedes:",allnodes,"\n"

Header = []
Header.append('filename')
for i in range(0, len(allnodes)):
    for j in range(0, len(allnodes)):
        Header.append(allnodes[i] + 'To' + allnodes[j])
print 'Header is long ', len(Header)

Fintime = []
dbcounter = 0

numApps = os.listdir('family/')

DatabaseRes = []
DatabaseRes.append(Header)

leng = len(numApps)
for i in range(0, len(numApps)):
    print 'starting ', i + 1, ' of ', leng
    if wf == 'Y':
        with open('family/' + str(numApps[i])) as callseq:  #Families/Trail1
            specificapp = []
            for line in callseq:

                specificapp.append(line.replace('\n', ''))
        callseq.close()
        #print "specificapp: ", specificapp
    else:
        specificapp = []
        for line in dbs[dbcounter][i]:
            specificapp.append(line)

    Startime = time()
    MarkMat = mk.main(specificapp, allnodes, wf)

    MarkRow = []
    if wf == 'Y':
        MarkRow.append(numApps[i])
    else:
        MarkRow.append(appslist[dbcounter][i])
    for i in range(0, len(MarkMat)):
        for j in range(0, len(MarkMat)):
            MarkRow.append(MarkMat[i][j])

    DatabaseRes.append(MarkRow)
    Fintime.append(time() - Startime)
dbcounter += 1
f = open('Features/' + WHICHCLASS + '/' + "result" ""+ '.csv', 'w')
for line in DatabaseRes:
    f.write(str(line).encode('utf-8') + '\n')
f.close