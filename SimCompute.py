# -*- coding: utf-8 -*-
from UserList import *
from UserInfo import *
# from os import *
import random
from FtSample import *
from FileUtil import *
import networkx as nx
import os as os
import string
import Queue
from math import *
import sys as sys


class SimCompute:
    per_parameter = 0.8
    per_Const = 0.9

    def __init__(self):
        self.ul = UserList()
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
        print "there is no file in type of " + fileDot
        return None

    def getInt(self,x):
        return int(x)

    def inQue(self,ID,q):
        flag=False
        if not q.qsize()==0:
            for i in range(q.qsize()):
                t = q.get()
                if t == ID:
                    flag = True
                q.put(t)
        return flag

    def preProcess(self,DATASET_PATH,perturb,directer,epsilon):
        # 1 从文件读取数据生成图
        # 2 生成各节点的出入邻点列表
        # 3 初始化出入度及排序
        # L=[]
        # attrNode = True
        # 从edge文件中读取数据创建图
        el = []
        nl = []
        if directer=='1':
            # 有向图
            G = nx.DiGraph()
            print "directedGraph "
            # 从文件读取数据生成有向图
            G=nx.read_adjlist(self.getFileFromSd(DATASET_PATH, "edge"),create_using=nx.DiGraph())
            #unicode转string
            for i in G.nodes():
                nl.append(i.encode("utf-8"))
            for i in G.edges():
                el.append((i[0].encode("utf-8"), i[1].encode("utf-8")))
            num = 0
            for i in nl:
                self.ul.addUser(str(i), UserInfo(i, num))
                num += 1
            # 加入出入邻点列表
            for i in el:
                self.ul.getUser(str(i[0])).adjOutList.append(i[1])
                self.ul.getUser(str(i[1])).adjInList.append(i[0])
            del G
            gc.collect()
        else:
            # 无向图
            G = nx.Graph()
            print "unDirecedGraph"
            # 从文件读取数据生成无向图
            G = nx.read_adjlist(self.getFileFromSd(DATASET_PATH, "edge"))
            # unicode字符转string
            for i in G.nodes():
                nl.append(i.encode("utf-8"))
            for i in G.edges():
                el.append((i[0].encode("utf-8"), i[1].encode("utf-8")))
            # 加入userList
            num=0
            for i in nl:
                self.ul.addUser(str(i), UserInfo(i, num))
                # L.append(UserInfo(i, num))
                num+=1
            # 加入出入邻点列表
            for i in el:
                self.ul.getUser(str(i[0])).adjOutList.append(i[1])
                self.ul.getUser(str(i[0])).adjInList.append(i[1])
                self.ul.getUser(str(i[1])).adjOutList.append(i[0])
                self.ul.getUser(str(i[1])).adjInList.append(i[0])
            del G
            gc.collect()
        del nl
        del el
        gc.collect()
        # print "memory ", sys.getsizeof(L)#/////////////////////////////////////////////////////////////////////////
        print "creating userlist finished "
        # 初始化出入度及排序
        self.sumLength = self.ul.initUserInfo(perturb, epsilon)

    def postProcessing(self, tuedge):
        # 之前生成的边
        edges1 = tuedge
        edges1.reverse()
        # 后处理生成的边
        edges2 = []
        pogra = nx.Graph()
        pogra.add_edges_from(list(set(edges1).union(set(edges2))))
        while not nx.is_connected(pogra):
            #         主体部分mgra
            mainedges = list(pogra.edges())
            print "pogra.edges", mainedges, "size", mainedges.__len__()
            #选择最新生成的边eqr
            eqr = edges1.pop(0)
            print "eqr",eqr
            vq = eqr[0]
            vr = eqr[1]
            ogra = nx.Graph()
    #         包含eqr的连通子图ogra，eqr所在的孤立点集
            for i in nx.connected_component_subgraphs(pogra):
                print "subgraph",i.edges()
                if (eqr in list(i.edges())) or ((vr,vq) in list(i.edges())):
                    ogra = i
                    break
            print "ogra",ogra.edges(),"size",ogra.edges().__len__()


            print "before main delete,",mainedges
            for i in list(ogra.edges()) :
                 print "i in loop main",i
                 if (i[0],i[1]) in mainedges:
                     mainedges.remove(i)
                 elif (i[1],i[0]) in mainedges:
                     mainedges.remove((i[1],i[0]))
                 else:
                     pass

            print  "mainedges",mainedges,"size",mainedges.__len__()
            mgra = nx.Graph()
            mgra.add_edges_from(mainedges)
            mseq=[]
            for i in mgra.nodes():
                for num in range(0,self.ul.getUser(i).o_degree):
                    mseq.append(i)
                    num+=1
            # pi(i)概率选vi
            vi = random.choice(mseq)
            lnode=[]
            lsim=[]
            for i in self.ul.getUser(vi).Prob_AdjList:
                lnode.append(i)
                lsim.append(self.ul.getUser(i).get1_simValue(i))
            # 选vj
            vj = self.prob(lnode,lsim)
            while self.ul.getUser(vj).i_degree<2 or not ((vi,vj) in edges1)or not ((vj,vi) in edges1) :
                vi = random.choice(mseq)
                lnode = []
                lsim = []
                for i in self.ul.getUser(vi).Prob_AdjList:
                    lnode.append(i)
                    lsim.append(self.ul.getUser(i).get1_simValue(i))
                vj = self.prob(lnode, lsim)
            # edges1.remove(eqr)
            print "vi",vi,"vj",vj
            print "edges1",edges1
            if (vi,vj) in edges1:
                edges1.remove((vi,vj))
                self.ul.getUser(vi).Prob_AdjList.remove(vj)
            else:
                edges1.remove((vj,vi))
                self.ul.getUser(vj).Prob_AdjList.remove(vi)
            edges2.append((vi,vr))
            self.ul.getUser(vi).Prob_AdjList.append(vr)
            edges2.append((vq,vj))
            self.ul.getUser(vq).Prob_AdjList.append(vj)
            pogra.clear()
            pogra.add_edges_from(list(set(edges1).union(set(edges2))))
        print "postprocessing finished "
        return list(set(edges1).union(set(edges2)))

    def prob(self,lnode, lsim):
        x = random.uniform(0, 1)
        cumulative_prob = 0.0
        for item, item_prob in zip(lnode, lsim):
            cumulative_prob += item_prob
            if x < cumulative_prob: break
        return item

    def generateUDLink(self, DATASET_PATH,dataSet):
        # 全体用户集
        userSet = self.ul.AllUser()
        sequence = []
        if self.sumLength %2==1:
            print "after perturbing ,sum of degree is odd,deal..."
            for i in userSet:
                if self.ul.getUser(i).o_degree>1:
                    self.ul.getUser(i).o_degree = self.ul.getUser(i).getODegree() - 1
                    break
        # 按照出度倍将用户加入sequence中
        for user in userSet:
            for num in range(0,self.ul.getUser(user).getODegree()):
                sequence.append(user)
        print "generating undirecedgraph"
        # 可能死循环的外层循环试过的点
        loop1=set()
        # 可能死循环的内层循环试过的点
        loop2 = set()
        while sequence :
            if loop1 | set(sequence) == loop1:
                print "step into endless loop"
                self.newdealUD(sequence)
                break
            # 选择ID1
            ID1=random.choice(sequence)
            node1 = self.ul.getUser(ID1)
            if node1.firstCandidateSorted:
                # 从候选集中选择IDn
                ftSample =  FtSample()
                seqNum = ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.weight)
                IDn = node1.firstCandidateSorted[seqNum]
                noden = self.ul.getUser(IDn)
                # 若IDn不在sequence中，重新选择IDn
                while not (IDn in sequence) :
                    node1.firstCandidateSorted.remove(IDn)
                    if not node1.firstCandidateSorted:
                        IDn=None
                        break
                    else:
                        IDn = node1.firstCandidateSorted[ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.weight)]
                        noden = self.ul.getUser(IDn)
                if not IDn==None:
                    edge = ID1 + " " + IDn
                    node1.Prob_AdjList.append(IDn)
                    noden.Prob_AdjList.append(ID1)
                    sequence.remove(ID1)
                    sequence.remove(IDn)
                    node1.firstCandidateSorted.remove(IDn)
                    noden.firstCandidateSorted.remove(ID1)
                    self.edges.append(edge)
            else:
                loop1.add(ID1)
                IDn=random.choice(sequence)
                noden = self.ul.getUser(IDn)
                loop2.add(IDn)
                # 如果ID1是IDn，或者IDn已经和ID1连成边，则重新选点
                while (ID1==IDn )or (IDn in node1.Prob_AdjList) or (ID1 in noden.Prob_AdjList):
                    IDn = random.choice(sequence)
                    noden = self.ul.getUser(IDn)
                    loop2.add(IDn)
                    if loop2|set(sequence)==loop2:
                        IDn = None
                        break
                if not IDn == None:
                    edge = ID1 + " " + IDn
                    loop1.remove(ID1)
                    node1.Prob_AdjList.append(IDn)
                    noden.Prob_AdjList.append(ID1)
                    sequence.remove(ID1)
                    sequence.remove(IDn)
                    self.edges.append(edge)
                #     不论是否生成边，都需要清空loop2
                loop2.clear()
            # print "edges",self.edges
        # print "剩余sequence", sequence
        # #后处理
        # # 根据edge生成gra判断连通性
        # gra = nx.Graph()
        # tuedge=[]
        # for i in self.edges:
        #     ea = i.split()
        #     a = (ea[0],ea[1])
        #     tuedge.append(a)
        # gra.add_edges_from(tuedge)#处理后边的顺序会乱，不按生成顺序
        # # el=list(gra.edges())
        # # print gra.edges()
        # # print "edges",self.edges
        # print "进行后处理的边",tuedge
        #
        # # tuedge.reverse()
        # # print tuedge
        # if (nx.is_connected(gra)):
        #     print "connected graph"
        # else:
        #     print "unconnected graph,begin postprocessing"
        #     self.edges=self.postProcessing(tuedge)
        print "sum of edges:",self.edges.__len__()
        futil = FileUtil()
        futil.writeTextFile(DATASET_PATH + dataSet + ".edges", self.edges)

    def newdealUD(self,sequence):
        kinl = []
        kins = []
        loop1=set()
        loop2=set()
        # 获取度满的节点
        kinl = self.ul.AllUser()
        for i in kinl:
            if i in sequence:
                kinl.remove(i)
        while (sequence):
            if loop1.__len__() ==sequence.__len__()*(sequence.__len__()-1):
                print "step into endless loop in dealing with endless loop,please try again"
                return
            #         选IDi
            IDi=random.choice(sequence)
            nodei = self.ul.getUser(IDi)
            #         选IDj
            IDj = random.choice(sequence)
            nodej = self.ul.getUser(IDj)
            # 若IDi只有一个，则不能被选两次
            while sequence.count(IDi) == 1 and IDi == IDj:
                IDj = random.choice(sequence)
                nodej = self.ul.getUser(IDj)
            loop1.add(IDi + " " + IDj)
            loop1.add(IDj + " " + IDi)
            # 根据度数加入序列
            for i in kinl:
                for num in range(0, self.ul.getUser(i).getODegree()):
                    kins.append(i)
            #选vk
            IDk = random.choice(kins)
            nodek = self.ul.getUser(IDk)
            IDl=None
            #选vl
            for i in self.ul.getUser(IDk).Prob_AdjList:
                if (i in kinl) and (not(i in self.ul.getUser(IDi).Prob_AdjList or i in self.ul.getUser(IDj).Prob_AdjList )):
                    IDl =i
                    nodel = self.ul.getUser(IDl)
                    break
            while IDl == None:
                # 选vk
                IDk = random.choice(kins)
                nodek = self.ul.getUser(IDk)
                loop2.add(IDk)
                # 选vl
                for i in self.ul.getUser(IDk).Prob_AdjList:
                    if (i in kinl) and (not(i in self.ul.getUser(IDi).Prob_AdjList or i in self.ul.getUser(IDj).Prob_AdjList )):
                        IDl = i
                        nodel = self.ul.getUser(IDl)
                        break
                if loop2 | set(kinl) == loop2:
                    loop2.clear()
                    IDl == None
                    break
            if not IDl == None:
                # 连il,kj
                edge = IDk+" "+IDl
                # 无向边是IDk+" "+IDl
                if edge in self.edges:
                    self.edges.remove(IDk+" "+IDl)
                    edge1 = IDi+" "+IDl
                    nodei.Prob_AdjList.append(IDl)
                    nodel.Prob_AdjList.append(IDi)
                    edge2 = IDk+" "+IDj
                    nodek.Prob_AdjList.append(IDj)
                    nodej.Prob_AdjList.append(IDk)
                # 无向边是IDl + " " + IDk
                else:
                    self.edges.remove(IDl + " " + IDk)
                    edge1 = IDi + " " + IDk
                    nodei.Prob_AdjList.append(IDk)
                    nodek.Prob_AdjList.append(IDi)
                    edge2 = IDl + " " + IDj
                    nodel.Prob_AdjList.append(IDj)
                    nodej.Prob_AdjList.append(IDl)
                nodek.Prob_AdjList.remove(IDl)
                nodel.Prob_AdjList.remove(IDk)
                self.edges.append(edge1)
                self.edges.append(edge2)
                sequence.remove(IDi)
                sequence.remove(IDj)
                loop1.remove(IDi + " " + IDj)
                if not IDi==IDj:
                    loop1.remove(IDj + " " + IDi)
                if (nodei.getODegree()==nodei.Prob_AdjList.__len__()):
                    kinl.append(IDi)
                if (nodej.getODegree()==nodej.Prob_AdjList.__len__()):
                    kinl.append(IDj)

    def generateDLink(self, DATASET_PATH,dataSet):
        userSet = self.ul.AllUser()
        Outsequence =[]
        Insequence = []
        for user in userSet:
            for num in range(0,self.ul.getUser(user).getODegree()):
                Outsequence.append(user)
            for num in range(0,self.ul.getUser(user).getIDegree()):
                Insequence.append(user)
        print "generating directedgraph "
        loop1 = set()
        loop2 = set()
        while Outsequence and Insequence:
            # 若所有入度节点均已被选为ID1，处理死循环
            if loop1|set(Outsequence)==loop1:
                print "step into endless loop "
                self.newdealD(Outsequence, Insequence)
                break
            # 从出度节点集选一个用户做起始节点vi
            ID1 = random.choice(Outsequence)
            node1 = self.ul.getUser(ID1)
            if node1.firstCandidateSorted:
                ftSample =  FtSample()
                # 用ftsample依概率选择vj
                seqNum = ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.weight)
                IDn = node1.firstCandidateSorted[seqNum]
                while not IDn in Insequence:
                    node1.firstCandidateSorted.remove(IDn)#候选集中去除IDn
                    if not node1.firstCandidateSorted:#ID1候选集为空后，令IDn=None，ID1将在下一次被选中时进入if node1.firstCandidateSorted同级的else中
                        IDn=None
                        break
                    else:
                        # 重新用ftsample依概率选择vj
                        IDn = node1.firstCandidateSorted[ftSample.getPrizeIndex(node1.firstCandidateSorted, node1.weight)]
                if not IDn==None:
                    edge = ID1 + " " + IDn
                    node1.Prob_AdjList.append(IDn)
                    Outsequence.remove(ID1)
                    Insequence.remove(IDn)
                    node1.firstCandidateSorted.remove(IDn)
                    self.edges.append(edge)
            else:
                loop1.add(ID1)
                # 选择IDn
                IDn = random.choice(Insequence)
                loop2.add(IDn)
                # 若ID1与IDn是同一个点，或者ID1与IDn已经练成边，重新选择IDn
                while ID1==IDn or IDn in node1.Prob_AdjList:
                    IDn = random.choice(Insequence)
                    loop2.add(IDn)
                    if loop2|set(Insequence)==loop2:
                        IDn = None
                        break
                if not IDn==None:
                    edge = ID1 + " " + IDn
                    loop1.remove(ID1)
                    node1.Prob_AdjList.append(IDn)
                    Outsequence.remove(ID1)
                    Insequence.remove(IDn)
                    # 加入边集
                    self.edges.append(edge)
                loop2.clear()
        # print "edges,",self.edges
        print "sum of edges:" + str(self.edges.__len__())
        futil =FileUtil()
        futil.writeTextFile(DATASET_PATH + dataSet + ".edges", self.edges)

    def newdealD(self,Outsequence,Insequence):
        kinl = self.ul.AllUser()
        for i in kinl:
            if i in Outsequence or i in Insequence:
                kinl.remove(i)
        kins = []
        while (Outsequence and Insequence):
            for i in kinl:
                for num in range(0, self.ul.getUser(i).o_degree):
                    kins.append(i)
            #         选IDi
            IDi = random.choice(Outsequence)
            #         选IDj
            IDj = random.choice(Insequence)
            #选vk
            IDk = random.choice(kins)
            IDl=None
            #选vl
            for i in self.ul.getUser(IDk).Prob_AdjList:
                if (i in kinl)  and (not IDi+" "+i in self.edges or IDk+" "+IDj in self.edges ):
                    IDl =i
                    break
            while IDl == None:
                # 选vk
                IDk = random.choice(kins)
                # 选vl
                for i in self.ul.getUser(IDk).Prob_AdjList:
                    if (i in kinl) and (not IDi+" "+i in self.edges or IDk+" "+IDj in self.edges ):
                        IDl = i
                        break
            # 连il,kj
            self.edges.remove(IDk+" "+IDl)
            self.ul.getUser(IDk).Prob_AdjList.remove(IDl)
            edge1 = IDi+" "+IDl
            self.ul.getUser(IDi).Prob_AdjList.append(IDl)
            edge2 = IDk+" "+IDj
            self.ul.getUser(IDk).Prob_AdjList.append(IDj)
            self.edges.append(edge1)
            self.edges.append(edge2)
            Outsequence.remove(IDi)
            Insequence.remove(IDj)
            if not ( IDi in Outsequence):
                kinl.append(IDi)
            if not( IDj in Insequence):
                kinl.append(IDj)
        #         只剩出度
        while (Outsequence):
            for i in kinl:
                for num in range(0, self.ul.getUser(i).i_degree):
                    kins.append(i)
            #         选IDi
            IDi = random.choice(Outsequence)
            #         选IDl
            IDl = random.choice(kins)
            while (IDi+" "+IDl in self.edges):
                IDl = random.choice(kins)
            # 连il
            edge1 = IDi+" "+IDl
            self.ul.getUser(IDi).Prob_AdjList.append(IDl)
            self.edges.append(edge1)
            Outsequence.remove(IDi)
            if not ( IDi in Outsequence):
                kinl.append(IDi)
        #         只剩入度
        while (Insequence):
            for i in kinl:
                for num in range(0, self.ul.getUser(i).o_degree):
                    kins.append(i)
            #         选IDi
            IDi = random.choice(Insequence)
             #         选IDl
            IDl = random.choice(kins)
            while (IDl + " " + IDi in self.edges):
                IDl = random.choice(kins)
            # 连il
            edge1 = IDl + " " + IDi
            self.ul.getUser(IDl).Prob_AdjList.append(IDi)
            self.edges.append(edge1)
            Insequence.remove(IDi)
            if not (IDi in Insequence):
                 kinl.append(IDi)
























