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
import Queue
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
            for i in G.nodes():
                nl.append(i.encode("utf-8"))
            for i in G.edges():
                el.append((i[0].encode("utf-8"), i[1].encode("utf-8")))
            # 排序//////////////////////////////////////////////////////////////////////////////////////////////////
            # nl.sort(key=lambda x: string.atoi(x), reverse=False)
            # el.sort(key=lambda x: (string.atoi(x[0]), string.atoi(x[1])), reverse=False)
            # 加入userList
            # num = 0
            # with open(self.getFileFromSd(DATASET_PATH, "node")) as f:
            #     for l in f:
            #         nl.append(l.rstrip('\n').rstrip())
            #         self.ul.addUser(nl[num], UserInfo(nl[num], num))
            #         num += 1
            num = 0
            for i in nl:
                self.ul.addUser(str(i), UserInfo(i, num))
                num += 1
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
            for i in G.nodes():
                nl.append(i.encode("utf-8"))
            # fnode = open(self.getFileFromSd(DATASET_PATH, "node"),'r')
            # for line in fnode:
            #     nl.append(line)
            # fnode.close()
            # fname=self.getFileFromSd(DATASET_PATH, "node")
            # with open("D:/IDEA/DP-FTexperiment/dataSets/little/little.node","r+") as f:
            #     nl=f.readlines()
            # 生成userList
            # num=0
            # with open(self.getFileFromSd(DATASET_PATH, "node")) as f:
            #     for l in f:
            #         nl.append(l.rstrip('\n').rstrip())
            #         self.ul.addUser(nl[num], UserInfo(nl[num], num))
            #         num += 1

            # print "nodes",nl

            for i in G.edges():
                el.append((i[0].encode("utf-8"), i[1].encode("utf-8")))
            # nl.sort(key=lambda x: string.atoi(x), reverse=False)
            # el.sort(key=lambda x: (string.atoi(x[0]), string.atoi(x[1])), reverse=False)
            # 加入userList
            num=0
            for i in nl:
                self.ul.addUser(str(i), UserInfo(i, num))
                num+=1
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

        # print "degree",G.degree('5')
        # print "neighbor"
        # for i in G.neighbors('5'):
        #     print i

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
        # 全体用户集
        userSet = self.ul.AllUser()
        sequence = []
        if self.sumLength %2==1:
            print "扰动后度的和为奇数，不符合无向图的要求.正在进行处理。。。"
            ID1 = self.ul.getFirstNodeID(userSet)
            self.ul.getUser(ID1).o_degree = self.ul.getUser(ID1).getODegree() - 1
        # 按照出度倍将用户加入sequence中
        for user in userSet:
            for num in range(0,self.ul.getUser(user).getODegree()):
                sequence.append(user)
        # print "sequence.__len__()",sequence.__len__()
        # print "sequence", sequence
        print "正在生成无向图。。。"
        endless = False
        deal =  False
        while sequence and not endless:
            for user in sequence:
                while1end = True
                if self.ul.getUser(user).getID1select() == False:
                    while1end = False
                if while1end == True:
                    print "进入死循环，开始处理剩余节点"
                    deal = True
                    break
            if (deal == True):
                self.dealUD(sequence)
                break

            # 选择ID1
            radom = int(random.random()*sequence.__len__())
            ID1 = sequence[radom]
            if not sequence:
                break
            node1 = self.ul.getUser(ID1)
            node1.setID1select(True)#//////////////////////////////////
            if node1.firstCandidateSorted:
                # 从候选集中选择IDn
                ftSample =  FtSample()
                seqNum = ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.candidateSim)
                IDn = node1.firstCandidateSorted[seqNum]
                noden = self.ul.getUser(IDn)
                noden.setIDnselect(True)  # //////////////////////////////////
                # 若IDn不在sequence中，重新选择IDn
                while not (IDn in sequence) :
                    noden.setIDnselect(False)  # //////////////////////////////////
                    node1.firstCandidateSorted.remove(IDn)
                    if not node1.firstCandidateSorted:
                        IDn=None
                        break
                    else:
                        IDn = node1.firstCandidateSorted[ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.candidateSim)]
                        noden = self.ul.getUser(IDn)
                        noden.setIDnselect(True)  # //////////////////////////////////
                if not IDn==None:
                    edge = ID1 + " " + IDn
                    # print "edge", edge

                    node1.Prob_AdjList.append(IDn)
                    noden.Prob_AdjList.append(ID1)
                    # for i in self.ul.AllUser():
                    #     print i,"adj",self.ul.getUser(i).Prob_AdjList
                    # print ID1,"node1.Prob_AdjList",node1.Prob_AdjList
                    # print IDn,"noden.Prob_AdjList",noden.Prob_AdjList
                    sequence.remove(ID1)
                    sequence.remove(IDn)
                    node1.firstCandidateSorted.remove(IDn)
                    noden.firstCandidateSorted.remove(ID1)
                    for ID in sequence:
                        self.ul.getUser(ID).setIDnselect(False)
                    self.ul.getUser(ID1).setID1select(False)
                    # for user in userSet:
                    #     print user, "候选节点集", self.ul.getUser(user).firstCandidateSorted
                    #     print user,"已连边节点集",self.ul.getUser(user).Prob_AdjList
                    self.edges.append(edge)
                    # print "edge", edge
            else:
                radom = int(random.random() * sequence.__len__())
                IDn = sequence[radom]
                noden = self.ul.getUser(IDn)
                noden.setIDnselect(True)  # //////////////////////////////////
                # 如果ID1是IDn，或者IDn已经和ID1连成边，则重新选点
                # count=0
                while (ID1==IDn )or (IDn in node1.Prob_AdjList) or (ID1 in noden.Prob_AdjList):
                    noden.setIDnselect(False)
                    radom = int(random.random() * sequence.__len__())
                    # print "167radom", radom
                    IDn = sequence[radom]
                    noden = self.ul.getUser(IDn)
                    noden.setIDnselect(True)  # //////////////////////////////////
                    for user in sequence:
                        while2end = True
                        if self.ul.getUser(user).getIDnselect ==False:
                            while2end = False
                        if while2end == True:
                            IDn=None
                            break
                if not IDn == None:
                    edge = ID1 + " " + IDn
                    # print "edge", edge
                    self.ul.getUser(ID1).setID1select(False)
                    node1.Prob_AdjList.append(IDn)
                    noden.Prob_AdjList.append(ID1)
                    # for i in self.ul.AllUser():
                    #     print i,"adj",self.ul.getUser(i).Prob_AdjList
                    noden.firstCandidateSorted.remove(ID1)#//////////////////////////////////////////////////////
                    sequence.remove(ID1)
                    sequence.remove(IDn)
                    self.edges.append(edge)
                #     不论是否生成边，都需要重置IDnselect
                for ID in sequence:
                    self.ul.getUser(ID).setIDnselect(False)
            # print "edges",self.edges

        # print "剩余sequence", sequence
        #后处理
        # gra = nx.Graph()
        # for i in self.edges:
        #     gra.add_edge(i[0],i[1])
        # # l=list(self.edges)
        # # gra.add_edges_from(l)
        # print gra.edges()
        # if (nx.is_connnected(gra)):
        #     print "是连通图"
        # else:
        #     print "不是连通图，开始后处理"
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
        # print "Outsequence", Outsequence
        # print "Insequence", Insequence
        print "正在生成有向图。。。"

        endless = False
        deal = False

        while Outsequence and Insequence and (not endless):
            # 若所有入度节点均已被选为ID1，处理死循环
            for user in Outsequence:
                while1end = True
                if self.ul.getUser(user).getID1select() == False:
                    while1end = False
                if while1end == True:
                    print "进入死循环，开始处理剩余节点"
                    deal = True
                    break
            if (deal == True):
                self.dealD(Outsequence,Insequence)
                break

            # 从出度节点集选一个用户做起始节点vi
            radom = int(random.random()*Outsequence.__len__())#以π(i)概率随机取点
            ID1 = Outsequence[radom]
            node1 = self.ul.getUser(ID1)
            node1.setID1select(True)
            if node1.firstCandidateSorted:
                ftSample =  FtSample()
                # 用ftsample依概率选择vj
                seqNum = ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.candidateSim)
                IDn = node1.firstCandidateSorted[seqNum]
                noden = self.ul.getUser(IDn)
                noden.setIDnselect(True)
                while not IDn in Insequence:
                    noden.setIDnselect(False)
                    node1.firstCandidateSorted.remove(IDn)#候选集中去除IDn
                    if not node1.firstCandidateSorted:#ID1候选集为空后，令IDn=None，ID1将在下一次被选中时进入if node1.firstCandidateSorted同级的else中
                        IDn=None
                        break
                    else:
                        # 重新用ftsample依概率选择vj
                        IDn = node1.firstCandidateSorted[ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.candidateSim)]
                        noden = self.ul.getUser(IDn)
                        noden.setIDnselect(True)
                if not IDn==None:
                    edge = ID1 + " " + IDn
                    node1.Prob_AdjList.append(IDn)
                    Outsequence.remove(ID1)
                    Insequence.remove(IDn)
                    node1.firstCandidateSorted.remove(IDn)
                    for ID in Insequence:
                        self.ul.getUser(ID).setIDnselect(False)
                    self.ul.getUser(ID1).setID1select(False)
                    self.edges.append(edge)
                    # print "edge", edge

            else:
                # 选择IDn
                radom = int(random.random() * Insequence.__len__())
                IDn = Insequence[radom]
                noden = self.ul.getUser(IDn)
                noden.setIDnselect(True)
                # 若ID1与IDn是同一个点，或者ID1与IDn已经练成边，重新选择IDn
                while ID1==IDn or IDn in node1.Prob_AdjList:
                    noden.setIDnselect(False)
                    radom = int(random.random() * Insequence.__len__())
                    # print "232radom", radom
                    IDn = Insequence[radom]
                    noden = self.ul.getUser(IDn)
                    noden.setIDnselect(True)
                    for user in Insequence:
                        while2end = True
                        if self.ul.getUser(user).getIDnselect == False:
                            while2end = False
                        if while2end == True:
                            IDn = None
                            break
                if not IDn==None:
                    edge = ID1 + " " + IDn
                    # print "edge", edge
                    self.ul.getUser(ID1).setID1select(False)
                    node1.Prob_AdjList.append(IDn)
                    Outsequence.remove(ID1)
                    Insequence.remove(IDn)
                    # 加入边集
                    self.edges.append(edge)
                for ID in Insequence:
                    self.ul.getUser(ID).setIDnselect(False)

            # print "剩余Insequence",Insequence
            # print "剩余Outsequencr",Outsequence
        print "边集大小" + str(self.edges.__len__())
        futil =FileUtil()
        futil.writeTextFile(DATASET_PATH + dataSet + ".edges", self.edges)

    # 无向图剩余节点处理方法
    def dealUD(self,sequence):
        print "待处理节点为", sequence
        len_se = sequence.__len__()
        while sequence.__len__()>len_se/2:
            radom = int(random.random() * sequence.__len__())
            sequence.pop(radom)
        print "剔除一半节点后，剩余节点为",sequence
        while sequence:
            # 1 随机选择ID1
            radom = int(random.random() * sequence.__len__())
            ID1 = sequence[radom]
            node1 = self.ul.getUser(ID1)
            # 2 先在 sequence中（度不满）中找吸引力最大的
            # 初始值
            force=0
            IDn=ID1
            tmp = 0
            # 找符合要求的吸引力最大的点
            for i in sequence:
                if (not i == ID1) and (not i in node1.Prob_AdjList) :
                    # force[i] = node1.candidateSim.get(i)
                    tmp = node1.candidateSim.get(i)
                    # print tmp
                if (tmp>force):
                    force=tmp
                    IDn=i
            #         找到了
            if not IDn==ID1:
                edge = ID1 + " " + IDn
                # print "edge", edge
                node1.Prob_AdjList.append(IDn)
                self.ul.getUser(IDn).Prob_AdjList.append(ID1)
                # for i in self.ul.AllUser():
                #     print i, "adj", self.ul.getUser(i).Prob_AdjList
                # print ID1,"node1.Prob_AdjList", node1.Prob_AdjList
                # print IDn,"noden.Prob_AdjList", self.ul.getUser(IDn).Prob_AdjList
                sequence.remove(ID1)
                sequence.remove(IDn)
                self.edges.append(edge)
            else:
                # lt = node1.candidateSim.keys()
                # 3 当2中没找到符合要求的点时再找力最大的
                items = node1.candidateSim.items()
                backitems = [[v[1], v[0]] for v in items]
                backitems.sort(reverse=True)
                l = [backitems[i] for i in range(0, len(backitems))]
                IDn=None
                # print " node1.Prob_AdjList", node1.Prob_AdjList
                # print l
                for i in l:
                    IDn = i[1]
                    if (not IDn==ID1) and (not (IDn in node1.Prob_AdjList)) :
                        # IDn = l[i][1]
                        break
                if not IDn == None:
                    edge = ID1 + " " + IDn
                    # print "edge", edge
                    node1.Prob_AdjList.append(IDn)
                    self.ul.getUser(IDn).Prob_AdjList.append(ID1)
                    # for i in self.ul.AllUser():
                    #     print i,"adj",self.ul.getUser(i).Prob_AdjList

                    # print ID1,"node1.Prob_AdjList", node1.Prob_AdjList
                    # print IDn,"noden.Prob_AdjList", self.ul.getUser(IDn).Prob_AdjList
                    sequence.remove(ID1)
                    self.edges.append(edge)
    #有向图剩余节点处理方法
    def dealD(self,Outsequence,Insequence):
        # print "待处理入度节点为", Insequence
        # print "待处理出度节点为", Outsequence
        len_se = Insequence.__len__()
        while (Outsequence.__len__() +Insequence.__len__()> len_se):
            radom = int(random.random() * (Outsequence.__len__() +Insequence.__len__()))
            # 单数时剔除入度点
            if(radom%2==0):
                radom = int(random.random() * Insequence.__len__())
                Insequence.pop(radom)
            # 复数时剔除出度点
            else:
                radom = int(random.random() * Outsequence.__len__())
                Outsequence.pop(radom)
        # print "剔除一半节点后，剩余入度节点为", Insequence
        # print "剔除一半节点后，剩余出度节点为", Outsequence
        # 先处理出度节点
        while Outsequence:
            # 1 随机选择ID1
            radom = int(random.random() * Outsequence.__len__())
            ID1 = Outsequence[radom]
            node1 = self.ul.getUser(ID1)
            # 2 先从Outsequence（度不满）中选吸引力最大的
            force = 0#吸引力
            IDn = ID1
            tmp = 0
            # 找符合要求的吸引力最大的点
            for i in Insequence:
                if (not i == ID1) and (not i in node1.Prob_AdjList):
                    tmp = node1.candidateSim.get(i)
                if (tmp > force):
                    force = tmp
                    IDn = i
            #         找到了
            if not IDn == ID1:
                edge = ID1 + " " + IDn
                # print "edge", edge
                node1.Prob_AdjList.append(IDn)
                # self.ul.getUser(IDn).Prob_AdjList.append(ID1)
                # for i in self.ul.AllUser():
                #     print i, "adj", self.ul.getUser(i).Prob_AdjList
                # print ID1,"node1.Prob_AdjList", node1.Prob_AdjList
                # print IDn,"noden.Prob_AdjList", self.ul.getUser(IDn).Prob_AdjList
                Outsequence.remove(ID1)
                Insequence.remove(IDn)
                self.edges.append(edge)
            else:
                # lt = node1.candidateSim.keys()
                # 3 当2中没找到符合要求的点时再找力最大的
                items = node1.candidateSim.items()
                backitems = [[v[1], v[0]] for v in items]
                backitems.sort(reverse=True)
                l = [backitems[i] for i in range(0, len(backitems))]
                IDn = None
                # print " node1.Prob_AdjList", node1.Prob_AdjList
                # print l
                for i in l:
                    IDn = i[1]
                    if (not IDn == ID1) and (not (IDn in node1.Prob_AdjList)):
                        # IDn = l[i][1]
                        break
                if not IDn == None:
                    edge = ID1 + " " + IDn
                    # print "edge", edge
                    node1.Prob_AdjList.append(IDn)
                    # self.ul.getUser(IDn).Prob_AdjList.append(ID1)
                    # for i in self.ul.AllUser():
                    #     print i, "adj", self.ul.getUser(i).Prob_AdjList
                    Outsequence.remove(ID1)
                    self.edges.append(edge)
        #    处理剩余的Insequence
        while Insequence:
            # 1 随机选择IDn
            radom = int(random.random() * Outsequence.__len__())
            IDn = Insequence[radom]
            noden = self.ul.getUser(IDn)
            # 2 Insequence已空，直接在所有节点范围内找吸引力最大的点为ID1
            # # 初始值
            # force = 0  # 吸引力
            # IDn = ID1
            # tmp = 0
            # # 找符合要求的吸引力最大的点
            # for i in Insequence:
            #     if (not i == ID1) and (not i in node1.Prob_AdjList):
            #         # force[i] = node1.candidateSim.get(i)
            #         tmp = node1.candidateSim.get(i)
            #         # print tmp
            #     if (tmp > force):
            #         force = tmp
            #         IDn = i
            # #         找到了
            # if not IDn == ID1:
            #     edge = ID1 + " " + IDn
            #     print "edge", edge
            #     node1.Prob_AdjList.append(IDn)
            #     # self.ul.getUser(IDn).Prob_AdjList.append(ID1)
            #     for i in self.ul.AllUser():
            #         print i, "adj", self.ul.getUser(i).Prob_AdjList
            #     # print ID1,"node1.Prob_AdjList", node1.Prob_AdjList
            #     # print IDn,"noden.Prob_AdjList", self.ul.getUser(IDn).Prob_AdjList
            #     Outsequence.remove(ID1)
            #     Insequence.remove(IDn)
            #     self.edges.append(edge)
            # else:
            # lt = node1.candidateSim.keys()
            # 3 当2中没找到符合要求的点时再找力最大的
            items = noden.candidateSim.items()
            backitems = [[v[1], v[0]] for v in items]
            backitems.sort(reverse=True)
            l = [backitems[i] for i in range(0, len(backitems))]
            ID1 = None
            # print " node1.Prob_AdjList", node1.Prob_AdjList
            # print l
            for i in l:
                ID1 = i[1]
                node1 = self.ul.getUser(ID1)
                if (not IDn == ID1) and (not (IDn in node1.Prob_AdjList)):
                    # IDn = l[i][1]
                    break
            if not IDn == None:
                edge = ID1 + " " + IDn
                # print "edge", edge
                node1.Prob_AdjList.append(IDn)
                # self.ul.getUser(IDn).Prob_AdjList.append(ID1)
                # for i in self.ul.AllUser():
                #     print i, "adj", self.ul.getUser(i).Prob_AdjList

                # print ID1,"node1.Prob_AdjList", node1.Prob_AdjList
                # print IDn,"noden.Prob_AdjList", self.ul.getUser(IDn).Prob_AdjList
                Insequence.remove(IDn)
                self.edges.append(edge)

    def inQue(self,ID,q):
        flag=False
        if not q.qsize()==0:
            for i in range(q.qsize()):
                t = q.get()
                if t == ID:
                    flag = True
                q.put(t)
        return flag





    def ge1UDLink(self, DATASET_PATH,dataSet):
        # 全体用户集
        userSet = self.ul.AllUser()
        sequence = []
        que = Queue.Queue()
        if self.sumLength % 2 == 1:
            print "扰动后度的和为奇数，不符合无向图的要求.正在进行处理。。。"
            ID1 = self.ul.getFirstNodeID(userSet)
            self.ul.getUser(ID1).o_degree = self.ul.getUser(ID1).getODegree() - 1
        # 按照出度倍将用户加入sequence中
        for user in userSet:
            for num in range(0, self.ul.getUser(user).getODegree()):
                sequence.append(user)
        num=0
        while (not sequence.__len__()==0) or (sequence.__len__()==0 and not que.qsize()==0):
            print "第", num, "次循环"
            num += 1
            # ID1
            if not que.empty():
                ID1 = que.get()
            else:
                ID1 = random.choice(sequence)
            node1 = self.ul.getUser(ID1)

            if node1.firstCandidateSorted:
                ftSample = FtSample()
                seqNum = ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.candidateSim)
                IDn = node1.firstCandidateSorted[seqNum]
                noden = self.ul.getUser(IDn)
                while (not IDn in sequence) and (not self.inQue(IDn,que)):
                    node1.firstCandidateSorted.remove(IDn)
                    if not node1.firstCandidateSorted:
                        IDn = None
                        break
                    else:
                        IDn = node1.firstCandidateSorted[ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.candidateSim)]
                if not IDn == None:
                    edge = ID1 + " " + IDn
                    node1.Prob_AdjList.append(IDn)
                    noden.Prob_AdjList.append(ID1)
                    if ID1 in sequence:
                        sequence.remove(ID1)
                    if IDn in sequence:
                        sequence.remove(IDn)
                    # sequence.remove(ID1)
                    # sequence.remove(IDn)
                    node1.firstCandidateSorted.remove(IDn)
                    noden.firstCandidateSorted.remove(ID1)
                    self.edges.append(edge)
                    print "edge",edge
            else:
                if not sequence.__len__() == 0:
                    IDn = random.choice(sequence)
                else:
                    IDn = que.get()
                noden = self.ul.getUser(IDn)
                if not ((IDn == ID1) or (IDn in node1.Prob_AdjList) or (ID1 in noden.Prob_AdjList)):
                    edge = ID1 + " " + IDn
                    node1.Prob_AdjList.append(IDn)
                    noden.Prob_AdjList.append(ID1)
                    if ID1 in sequence:
                        sequence.remove(ID1)
                    if IDn in sequence:
                        sequence.remove(IDn)
                    node1.firstCandidateSorted.remove(IDn)
                    noden.firstCandidateSorted.remove(ID1)
                    self.edges.append(edge)
                    print "edge", edge
                else:
                    print "append", ID1, " ", IDn
                    if ID1 in sequence:
                        sequence.remove(ID1)
                    if IDn in sequence:
                        sequence.remove(IDn)
                    # if(fromq == )
                    que.put(ID1)
                    que.put(IDn)
            print "sequence", sequence
            if (que.qsize() == 0):
                print "que", 0
            else:
                print "que size", que.qsize()
                for i in range(que.qsize()):
                    a = que.get()
                    print a
                    que.put(a)


        print "合成图边集大小" + str(self.edges.__len__())
        futil = FileUtil()
        futil.writeTextFile(DATASET_PATH + dataSet + ".edges", self.edges)

    def ge2UDLink(self, DATASET_PATH,dataSet):
        # 全体用户集
        userSet = self.ul.AllUser()
        sequence = []
        que = Queue.Queue()
        if self.sumLength % 2 == 1:
            print "扰动后度的和为奇数，不符合无向图的要求.正在进行处理。。。"
            ID1 = self.ul.getFirstNodeID(userSet)
            self.ul.getUser(ID1).o_degree = self.ul.getUser(ID1).getODegree() - 1
        # 按照出度倍将用户加入sequence中
        for user in userSet:
            for num in range(0, self.ul.getUser(user).getODegree()):
                sequence.append(user)
        num = 0
        print "sequence",sequence
        while (not sequence.__len__()==0) or (sequence.__len__()==0 and not que.qsize()==0) :
            print "第",num,"次循环"
            num+=1
            if not que.empty():
                ID1 = que.get()
            else:
                ID1 = random.choice(sequence)
            node1 = self.ul.getUser(ID1)
            if not sequence.__len__()==0:
                IDn = random.choice(sequence)
            else:
                IDn = que.get()
            noden = self.ul.getUser(IDn)
            if not (( IDn == ID1) or (IDn in node1.Prob_AdjList) or (ID1 in noden.Prob_AdjList)):
                edge = ID1 + " " + IDn
                print "edge",edge
                node1.Prob_AdjList.append(IDn)
                noden.Prob_AdjList.append(ID1)
                if ID1 in sequence:
                    sequence.remove(ID1)
                if IDn in sequence:
                    sequence.remove(IDn)
                self.edges.append(edge)
            else:
                print "append",ID1," ",IDn
                if ID1 in sequence:
                    sequence.remove(ID1)
                if IDn in sequence:
                    sequence.remove(IDn)
                # if(fromq == )
                que.put(ID1)
                que.put(IDn)
            print "sequence",sequence
            if( que.qsize()==0):
                print "que",0
            else:
                print "que size",que.qsize()
                for i in range(que.qsize()):
                    a=que.get()
                    print a
                    que.put(a)





















