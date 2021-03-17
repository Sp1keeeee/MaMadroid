# MaMadroid
A new version used Androguard but not Soot to realize MaMadroid

原项目链接：https://bitbucket.org/gianluca_students/mamadroid_code/src/master/

本项目在原项目的基础上进行了修改，使用androguard而非soot对APK进行静态分析获取API调用。

## 环境

Python2.7和Androguard3.3.5。

## 代码文件说明

- **mamadroid.py**：本项目第一个执行的脚本，通过此脚本把apk文件下的所有apk首先通过androguard转换为gml文件（调用图文件）存放到gml文件夹下【apk2graph.extractcg】，然后通过【gml2txt.gml2graph】读取图中的信息得到图中的节点和边，通过【gml2txt.caller2callee】转换为存储调用的对应.txt文件存储在txtfile文件夹下，最后一步通过【abstractGraph._preprocess_graph】将txt文件进行抽象，抽象出来的文件分别存储在class、family和package文件夹下。

  - **apk2graph.py**：通过使用androguard把目标为apkpath的APK转换为API调用图存储在路径为gmlpath的gml文件中。

  - **gml2txt.py**: gml2graph函数通过读取gml文件得到调用图中的所有节点以及边信息，caller2callee通过调用parse.py中的方法将gml文件中的调用图信息转换为txt文件。

    - **parse.py**:解析gml文件中各个节点中的label转换为A.B.C...的形式。

  - **abstractGraph.py**: 把API调用抽象为class和family模式，主要过程是首先通过class.txt把每个文件调用图对应的txt文件抽象成class然后通过Packages.txt和Families.txt将其抽象为包和家族文件存放到package和family文件夹中对应的文件中。

    

- **FamilyfoMak.py**: 通过Families11.txt文件作为名单调用Markov.py把family文件夹下的文件转换为马尔可夫矩阵存放到Features/Families文件夹下。

- **PackagetoMak.py**: 通过Families11.txt文件作为名单调用Markov.py把family文件夹下的文件转换为马尔可夫矩阵存放到Features/Packages/文件夹下。

- **Markov.py**: 读取不同模式得到的抽象后的txt文件转换为马尔可夫矩阵。

## 文件及文件夹说明

**classes.txt、Families.txt、Families11.txt**、**Packages.txt**：自定义参考文件。

**log.txt**:apk转换为gml成功的记录。

其余文件夹初始都为空，在apk文件夹下加入apk后即可运行第一个脚本文件。

程序中还有很多不足，如有错误，可以联系我的邮箱。