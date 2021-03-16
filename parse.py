'''
info:解析gml文件中各个节点中的label转换为A.B.C...的形式
'''
from collections import defaultdict

def parse_label(line): #parse label to api
    str = ""
    nclass = ""
    nfunction = ""
    if(line.startswith("L")):
        str = line[1:]
    else:
        str = line
    #print str
    str = str.rpartition("->")
    nclass = str[0]
    nfunction = str[2]
    #print nfunction
    nclass = nclass[0:-1]
    nclass = nclass.replace('/','.')
    nfunction = nfunction.rpartition(")")
    type = nfunction[2].rpartition('[')[0]
    nfunction = type + nfunction[0] + nfunction[1]
    api = "<" + nclass + ": " +nfunction + ">"

    return api


if __name__ == '__main__':
    line = "Lcom/unipay/account/UnipayAccountPlatform;->refreshPoint(Landroid/os/Handler;)V [access_flags=public] @ 0x18e4cc"
    line2 = "Ljava/util/concurrent/locks/ReentrantLock;-><init>()V"
    line3 = "Lu/aly/dg;->l()Lu/aly/db; [access_flags=public abstract] @ 0x0"

    parse_label(line2)
    parse_label(line3)