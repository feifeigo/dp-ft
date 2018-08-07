# -*- coding: utf-8 -*-
from UserList import *
from UserInfo import *
from AttributeList import *
# from os import *
import random
from FtSample import *
from FileUtil import *
import networkx as nx
import os as os
import string
from math import *

class SimCompute:
    # attribute disturb
    per_parameter = 0.8
    per_Const = 0.9

    def __init__(self):
        self.ul = UserList()
        # self.al = AttributeList()
        self.edges = []
        self.sumLength = 0

    # 搜索目录下文件，不搜索子目录下的文件
    def getFileFromSd(self,pa,fileDot):
        for f in os.listdir(pa):
            fn, ft = os.path.splitext(f)
            if ft == ('.'+fileDot):
                thepath = pa+'/'+ f
                print thepath
                return thepath
        print "该社交网络不存在" + fileDot + "类型文件"
        return None

    def getInt(self,x):
        return int(x)

    def preProcess(self,DATASET_PATH,perturb,directer,epsilon):
        # 1 从文件读取数据生成图
        # 2 生成各节点的出入邻点列表
        # 3 初始化出入度及排序

        # attrNode = True
        # 从edge文件中读取数据创建图
        if directer=='1':
            # 有向图
            G = nx.DiGraph()
            print "direcedGraph"
            # 从文件读取数据生成有向图
            G=nx.read_adjlist(self.getFileFromSd(DATASET_PATH, "edge"),create_using=nx.DiGraph())
            el = []
            nl = []
            #unicode转string
            # for i in G.nodes():
            #     nl.append(i.encode("utf-8"))
            for i in G.edges():
                el.append((i[0].encode("utf-8"), i[1].encode("utf-8")))
            # 排序//////////////////////////////////////////////////////////////////////////////////////////////////
            # nl.sort(key=lambda x: string.atoi(x), reverse=False)
            # el.sort(key=lambda x: (string.atoi(x[0]), string.atoi(x[1])), reverse=False)
            # 加入userList
            num = 0
            with open(self.getFileFromSd(DATASET_PATH, "node")) as f:
                for l in f:
                    nl.append(l.rstrip('\n').rstrip())
                    self.ul.addUser(nl[num], UserInfo(nl[num], num))
                    num += 1
            # num = 0
            # for i in nl:
            #     self.ul.addUser(str(i), UserInfo(i, num))
            #     num += 1
            # 加入出入邻点列表
            for i in el:
                self.ul.getUser(str(i[0])).adjOutList.append(i[1])
                self.ul.getUser(str(i[1])).adjInList.append(i[0])
        else:
            # 无向图
            G = nx.Graph()
            print "unDirecedGraph"
            # 从文件读取数据生成无向图
            G = nx.read_adjlist(self.getFileFromSd(DATASET_PATH, "edge"))
            el = []
            nl = []
            # unicode字符转string
            # for i in G.nodes():
            #     nl.append(i.encode("utf-8"))
            # fnode = open(self.getFileFromSd(DATASET_PATH, "node"),'r')
            # for line in fnode:
            #     nl.append(line)
            # fnode.close()
            # fname=self.getFileFromSd(DATASET_PATH, "node")
            # with open("D:/IDEA/DP-FTexperiment/dataSets/little/little.node","r+") as f:
            #     nl=f.readlines()
            # 生成userList
            num=0
            with open(self.getFileFromSd(DATASET_PATH, "node")) as f:
                for l in f:
                    nl.append(l.rstrip('\n').rstrip())
                    self.ul.addUser(nl[num], UserInfo(nl[num], num))
                    num += 1

            # print "nodes",nl

            for i in G.edges():
                el.append((i[0].encode("utf-8"), i[1].encode("utf-8")))
            # nl.sort(key=lambda x: string.atoi(x), reverse=False)
            # el.sort(key=lambda x: (string.atoi(x[0]), string.atoi(x[1])), reverse=False)
            # 加入userList
            # num=0
            # for i in nl:
            #     self.ul.addUser(str(i), UserInfo(i, num))
            #     num+=1
            # 加入出入邻点列表
            for i in el:
                self.ul.getUser(str(i[0])).adjOutList.append(i[1])
                self.ul.getUser(str(i[0])).adjInList.append(i[1])
                self.ul.getUser(str(i[1])).adjOutList.append(i[0])
                self.ul.getUser(str(i[1])).adjInList.append(i[0])
        print "创建用户列表成功"
        # 初始化出入度及排序
        self.sumLength = self.ul.initUserInfo(perturb, epsilon)
        print "没有写属性相关操作，该社交网络为无属性的简单图"

    # def computeErrorProcess(self): print "computeErrorProcess has not finished"

    # def generateAttribute(self,DATASET_PATH,dateSet, epsilon2):
    #     userSet = self.ul.AllUser()
    #     attInfo = []
    #     actInfo = []
    #     for user in userSet:
    #         u = self.ul.getUser(user)
    #         u.setNumOfAff()
    #         u.setPerNumOfAff(epsilon2)
    #         while(not u.Prob_Affiliation):
    #             i = 0
    #             # 用户user的所有属性的聚集系数
    #             # for att in self.ul.getUser(user).Affiliation:
    #     print "generateAttribute has not finished"

    def generateUDLink(self, DATASET_PATH,dataSet):
        userSet = self.ul.AllUser()
        sequence = []
        if self.sumLength %2==1:
            print "扰动后度的和为奇数，不符合无向图的要求.正在进行处理。。。"
            ID1 = self.ul.getFirstNodeID(userSet)
            self.ul.getUser(ID1).o_degree = self.ul.getUser(ID1).getODegree() - 1
        # 按照出度倍将用户加入sequence中
        for user in userSet:
            print user,"候选节点集",self.ul.getUser(user).firstCandidateSorted
            for num in range(0,self.ul.getUser(user).getODegree()):
                sequence.append(user)
        # print "sequence.__len__()",sequence.__len__()
        print "sequence", sequence
        print "正在生成无向图。。。"

        while sequence:
            # 选择ID1
            radom = int(random.random()*sequence.__len__())
            ID1 = sequence[radom]
            if not sequence:
                break
            node1 = self.ul.getUser(ID1)
            if node1.firstCandidateSorted:
                # 从候选集中选择IDn
                ftSample =  FtSample()
                seqNum = ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.candidateSim)
                IDn = node1.firstCandidateSorted[seqNum]
                noden = self.ul.getUser(IDn)
                # 若IDn不在sequence中，重新选择IDn
                while not (IDn in sequence) :
                    node1.firstCandidateSorted.remove(IDn)
                    if not node1.firstCandidateSorted:
                        IDn=None
                        break
                    else:
                        IDn = node1.firstCandidateSorted[ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.candidateSim)]
                if not IDn==None:
                    edge = ID1 + " " + IDn
                    print "edge", edge

                    node1.Prob_AdjList.append(IDn)
                    noden.Prob_AdjList.append(ID1)
                    sequence.remove(ID1)
                    sequence.remove(IDn)
                    node1.firstCandidateSorted.remove(IDn)
                    noden.firstCandidateSorted.remove(ID1)
                    # for user in userSet:
                    #     print user, "候选节点集", self.ul.getUser(user).firstCandidateSorted
                    #     print user,"已连边节点集",self.ul.getUser(user).Prob_AdjList
                    self.edges.append(edge)
                    # print "edge", edge
            else:
                radom = int(random.random() * sequence.__len__())
                IDn = sequence[radom]
                noden = self.ul.getUser(IDn)
                # 如果ID1是IDn，或者IDn已经和ID1连成边
                count=0
                while (ID1==IDn )or (IDn in node1.Prob_AdjList) or (ID1 in noden.Prob_AdjList):
                    radom = int(random.random() * sequence.__len__())
                    # print "167radom", radom
                    IDn = sequence[radom]
                    count+=1
                    if count>30:
                        IDn=None
                        break
                if not IDn == None:
                    edge = ID1 + " " + IDn
                    print "edge", edge
                    node1.Prob_AdjList.append(IDn)
                    noden.Prob_AdjList.append(ID1)
                    noden.firstCandidateSorted.remove(ID1)#//////////////////////////////////////////////////////
                    sequence.remove(ID1)
                    sequence.remove(IDn)
                    # for user in userSet:
                    #     print user, "候选节点集", self.ul.getUser(user).firstCandidateSorted
                    #     print user, "已连边节点集", self.ul.getUser(user).Prob_AdjList
                    self.edges.append(edge)
                    # print "edge", edge

            print "剩余sequence", sequence
        print "合成图边集大小" + str(self.edges.__len__())
        futil = FileUtil()
        futil.writeTextFile(DATASET_PATH + dataSet + ".edges", self.edges)

    def generateDLink(self, DATASET_PATH,dataSet):
        userSet = self.ul.AllUser()
        Outsequence =[]
        Insequence = []

        for user in userSet:
            for num in range(0,self.ul.getUser(user).getODegree()):
                Outsequence.append(user)
            for num in range(0,self.ul.getUser(user).getIDegree()):
                Insequence.append(user)
        # print "出度和" + str(Outsequence.__len__())
        # print "入度和" + str(Insequence.__len__())
        print "Outsequence", Outsequence
        print "Insequence", Insequence
        print "正在生成有向图。。。"

        while Outsequence and Insequence:
            # 从出度节点集选一个用户做起始节点vi
            radom = int(random.random()*Outsequence.__len__())#论文中说以π(i)概率随机取点
            ID1 = Outsequence[radom]
            node1 = self.ul.getUser(ID1)
            if node1.firstCandidateSorted:
                ftSample =  FtSample()
                # 用ftsample依概率选择vj
                seqNum = ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.candidateSim)
                IDn = node1.firstCandidateSorted[seqNum]
                while not IDn in Insequence:
                    node1.firstCandidateSorted.remove(IDn)#候选集中去除IDn
                    if not node1.firstCandidateSorted:#ID1候选集为空后，令IDn=None，ID1将在下一次被选中时进入if node1.firstCandidateSorted同级的else中
                        IDn=None
                        break
                    else:
                        # 重新用ftsample依概率选择vj
                        IDn = node1.firstCandidateSorted[ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.candidateSim)]

                if not IDn==None:
                    edge = ID1 + " " + IDn
                    node1.Prob_AdjList.append(IDn)
                    Outsequence.remove(ID1)
                    Insequence.remove(IDn)
                    node1.firstCandidateSorted.remove(IDn)
                    self.edges.append(edge)
                    print "edge", edge

            else:
                # 选择IDn
                radom = int(random.random() * Insequence.__len__())
                IDn = Insequence[radom]
                # 若ID1与IDn是同一个点，或者ID1与IDn已经练成边，重新选择IDn
                while ID1==IDn or IDn in node1.Prob_AdjList:
                    radom = int(random.random() * Insequence.__len__())
                    # print "232radom", radom
                    IDn = Insequence[radom]
                edge = ID1 + " " + IDn
                node1.Prob_AdjList.append(IDn)
                Outsequence.remove(ID1)
                Insequence.remove(IDn)
                # 加入边集
                self.edges.append(edge)
                print "edge", edge

        print "边集大小" + str(self.edges.__len__())
        futil =FileUtil()
        futil.writeTextFile(DATASET_PATH + dataSet + ".edges", self.edges)



















