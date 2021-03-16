#coding=utf-8
'''
info: 把API调用抽象为class和family模式，主要过程是首先通过class.txt把每个文件调用图对应的txt文件抽象成class然后通过Packages.txt和Families.txt将其抽象为包和家族文件存放到package和family文件
夹中对应的文件中
'''
import os
from multiprocessing import Process

def _preprocess_graph(app, _dir):
	''' gets and clean the callers and callees'''

	appl = app.split("/")[-1]   #appl:当前目录下的一个临时文件
	with open(appl, 'w') as fp:
		with open(app) as fh:
			for lines in fh:
# 例如某一行为<com.gionee.account.sdk.GioneeAccount: Z isTnLogin()> ==> ['<com.gionee.account.sdk.GioneeAccount: Ljava/lang/String; getUsername()>\n', '<android.text.TextUtils: isEmpty(Ljava/lang/CharSequence;)>\n']
				caller = ""
				callee = []
				line = lines.split(" ==> ")#将调用者 与 被调用者分开
				caller = line[0].split(":")[0].replace("<", "")#取调用者的class名
				if "," in str(line[1]):   # 被调用者存在多个
					subc = line[1].split("\\n',")#将多个被调者分开
					for i in subc:
						subCallees = i.split(":")  #提取被调用者中的class
						if "[" in subCallees[0]: #处理后放入callee中
							callee.append(subCallees[0].replace("['<", "").strip())
						else:
							callee.append(subCallees[0].replace("'<", "").strip())
				else:					#只存在一个被调用者
					callee.append(line[1].split(":")[0].replace("['<", "").strip())
				fp.write(caller + "\t")  #调用者写入临时文件
				_length = len(callee)
				for a in range(_length): #将被调用者写入临时文件
					if a < _length - 1:
						fp.write(str(callee[a]).strip('"<') + "\t")
					else:
						fp.write(str(callee[a]).strip('"<') + "\n")
	selfDefined(appl, _dir)


def selfDefined(f, _dir): #f:包含调用者和被调用者的临时文件 _dir：当前目录文件
	''' calls all three modes of abstraction '''

	Package = []
	Family = []
	Class = []
	#将自定义的包、家族以及类加入到上面的数组中
	with open("Packages.txt") as fh:
		for l in fh:
			if l.startswith('.'):
				Package.append(l.strip('\n').lstrip('.'))
			else:
				Package.append(l.strip('\n').strip())
	with open("Families.txt") as fh:
		for l in fh:
			Family.append(l.strip('\n').strip())
	with open("classes.txt") as fh:
		for l in fh:
			Class.append(l.strip('\n').strip())
	ff = abstractToClass(Class, f, _dir) #ff为提取的class的文件
	os.remove(f)#删除临时文件
	Package.reverse()
	fam = Process(target = abstractToMode, args=(Family, ff, _dir))
	fam.start()
	pack = Process(target=abstractToMode, args=(Package, ff, _dir))
	pack.start()
	pack.join()


def _repeat_function(lines, P, fh, _sep): #lines：处理过后的对应文件中每一行包含的每一个数据 P：自定义的class文件（相当于一个名单）fh：某一个APP对应的class文件夹中的文件 _sep：制表符
	if lines.strip() in P:  #如果在名单中写入class文件夹中的文件
		fh.write(lines.strip() + _sep)
	else:    #如果不在名单中
		if "junit." in lines: #对一些特殊字符串的处理
			return
		if '$' in lines:
			if lines.replace('$', '.') in P:
				fh.write(lines.replace('$', '.') + _sep)
				return
			elif lines.split('$')[0] in P:
				fh.write(lines.split('$')[0] + _sep)
				return
		items = lines.strip().split('.')
		item_len = len(items)
		count_l = 0
		for item in items:
			if len(item) < 3:
				count_l += 1
		if count_l > (item_len / 2):#字符小于3个的大于整体个数的二分之一 就认定为混淆
			fh.write("obfuscated" + _sep)
		else:
			fh.write("self-defined" + _sep) #否则为自定义


def abstractToClass(_class_whitelist, _app, _dir):#_class_whitelist：自定义的class文件 _app:包含调用者和被调用者的临时文件 _dir：当前目录文件
	''' abstracts the API calls to classes '''

	newfile = _dir + "/class/" + _app.split('/')[-1]
	with open(newfile, 'w') as fh:
		with open(_app) as fp:
			for line in fp:
				lines = line.strip('\n').split('\t')
				lines = [jjj for jjj in lines if len(jjj) > 1] # ensures each caller or callee is not a single symbol e.g., $
				num = len(lines)
				for a in range(num): #将得到的class写入class文件夹下的文件中
					if a < num - 1:
						_repeat_function(lines[a], _class_whitelist, fh, "\t")
					else:
						_repeat_function(lines[a], _class_whitelist, fh, "\n")

	return newfile


def abstractToMode(_whitelist, _app, _dir): #_whitelist：自定义的名单 _app：抽象的class文件 _dir：当前文件目录
	''' abstracts the API calls to either package or family '''

	dico = {"org.xml": 'xml', "com.google":'google', "javax": 'javax', "java": 'java', "org.w3c.dom": 'dom', "org.json": 'json',\
 "org.apache": 'apache', "android": 'android', "dalvik": 'dalvik'}
	family = False
	if len(_whitelist) > 15: #通过名单长度判断是family模式还是package模式 然后在对应文件夹创建对应APP对应模式的文件
		newfile = _dir + "/package/" + _app.split('/')[-1]
	else:
		newfile = _dir + "/family/" + _app.split('/')[-1]
		family = True

	with open(newfile, 'w') as fh:
		with open(_app) as fp:
			for line in fp:
				lines = line.strip('\n').split('\t')
				for items in lines:
					if "obfuscated" in items or "self-defined" in items:
						fh.write(items + '\t')
					else:
						for ab in _whitelist:
							if items.startswith(ab):#通过startwith进行判断
								if family: # if True, family, otherwise, package
									fh.write(dico[ab] + '\t')
								else:
									fh.write(ab + '\t')
								break
				fh.write('\n')
