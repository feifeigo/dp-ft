# -*- coding: utf-8 -*-
from numpy import *
from math import *
import string
import sys as sys
import gc as gc

class UserList:
    alpha = float(0.75)
    IN_DEGREE = 1
    OUT_DEGREE = 2
    index = 2 #index 对应于论文中公式2-9的伽马
    walk_step = 2

    def __init__(self):
        self.userList = {}

    def AllUser(self):
        lt = self.userList.keys()
        return lt

    def setUserList(self,userList):
        self.userList = userList

    def getUser(self,id):
        return self.userList.get(id)

    def addUser(self, key, value):
        self.userList[key]=value

    def count_n_hop_neighbor(self,u,hop):
        for i in range(1,hop):
            for i in u.AllHip1User():
                u.n_hop_neighbor=list(set(u.n_hop_neighbor).union(set(self.getUser(i).AllHip1User())))

    def LRW(self,u,tempMatrix,simMatrix,transMatrix):
        seq2id = {}
        id2seq = {}
        # 建立用户ID与int型seq的对应关系
        seq = 0
        for user in u.n_hop_neighbor:
            seq2id[seq] = user
            id2seq[user] = seq
            seq+=1
        n_hop_neighbor_size = u.n_hop_neighbor.__len__()
        # 采用一步转移概率矩阵作为社交网络节点间的初始相关度矩阵
        for i in range(0,n_hop_neighbor_size):
            for j in range(0,n_hop_neighbor_size):
                # 若i，j对应的用户为邻点
                if seq2id.get(j) in (self.getUser(seq2id.get(i))).AllHip1User():
                    transMatrix[i,j]=self.getUser(seq2id.get(i)).get1_simValue(seq2id.get(j))
                else:
                    pass
        # 初始化第一步的simMatrix
        simMatrix = transMatrix
        tempMatrix = transMatrix
        # 随机游走
        for i in range(1,self.walk_step):
            tempMatrix = simMatrix* transMatrix
            simMatrix = simMatrix+ tempMatrix
        #起点用户
        target_user_seq = id2seq.get(u.ID)
        for sequence in range(n_hop_neighbor_size):
            v_id=seq2id.get(sequence)
            sim_uv= simMatrix[target_user_seq,sequence]
            v=self.getUser(v_id)
            # force compute吸引力的计算
            vd= v.getIDegree()
            weight=math.pow(sim_uv, self.index) * vd
            # save the corelation
            u.add_Cor(v_id, sim_uv)
            # 保存节点间的力
            u.add_wei(v_id, weight)

    # initialazation. includes: 1-step correlation and random walk
    def initUserInfo(self,perturb,epsilon):
        userSet = self.AllUser()#排序后userset
        ousumEdge = 0
        insumEdge = 0
        # 计算入度和出度和
        for ID in userSet:
            u = self.getUser(ID)
            u.setDegree()#设置了out_degree和in_dgree（原图）
            # 属性相关用不上
            ousumEdge += u.getOutDegree()
            insumEdge += u.getInDegree()
        print "sum of odegree " , ousumEdge , "sum of idegree " , insumEdge
        # 为每个用户初始化one - hop相关度
        for anUserSet in userSet:
            sum = 0.0
            u = self.getUser(anUserSet)
            # 概率计算，公式2-6右部分
            if u.adjInList:
                for a in u.adjInList:
                    sim_ku = (1.0 - self.alpha) / u.in_degree
                    val = u.get1_simValue(a) + sim_ku
                    u.add_Sim(a, val)
            #  概率计算，公式2-6左部分
            if u.adjOutList:
                for a in u.adjOutList:
                    sim_ku = float(self.alpha / u.out_degree)
                    u.add_Sim(a, (u.get1_simValue(a) + sim_ku))
            # 初始化概率归一化处理
            for a in u.candidateSim.keys():
                sum += u.candidateSim.get(a)
            if not sum == 0.0:
                for a in u.candidateSim.keys():
                    value = u.candidateSim.get(a)
                    u.add_Sim(a, (value / sum))
        print "the initialzation of corelation transition probability finished"
        # L=[]
        numofv=userSet.__len__()
        osumEdge = 0
        isumEdge = 0
        size = 0
        for anUserSet in userSet:
            u = self.getUser(anUserSet)
            for i in u.AllHip1User():
                # 出度邻点以及入度邻点
                u.n_hop_neighbor.append(i)
            # n次后邻点
            self.count_n_hop_neighbor(u, self.walk_step)
            size = size if (u.n_hop_neighbor.__len__()<size) else u.n_hop_neighbor.__len__()
        tempMatrix = mat(zeros((size, size)))
        simMatrix = mat(zeros((size, size)))  # 相关度矩阵
        transMatrix = mat(zeros((size, size)))
        # call random walk correlation computation, you can change the walk_step
        ilrw=0
        for anUserSet in userSet:
            u = self.getUser(anUserSet)
            # 为节点施加度差分隐私保护
            u.setPeDegree(perturb, epsilon,numofv)
            # 基于LRW的节点间相关度计算
            self.LRW(u,tempMatrix,simMatrix,transMatrix)
            osumEdge += u.getODegree()
            isumEdge += u.getIDegree()
            ilrw+=1
            if ilrw%1000==0:
                print "no.",ilrw,"node finised lrw"
            # L.append(u)
        del tempMatrix
        del simMatrix
        del transMatrix
        gc.collect()
        # print "memory ", sys.getsizeof(L)
        change = osumEdge-isumEdge
        # 出度大，加入度
        while(change>0):
            uc=random.choice(userSet)
            if(self.getUser(uc).i_degree < numofv - 1):
                self.getUser(uc).i_degree+=1
                change-=1
                isumEdge+=1
        # 入度大，加出度
        while (change < 0):
            uc = random.choice(userSet)
            if (self.getUser(uc).o_degree < numofv - 1):
                self.getUser(uc).o_degree += 1
                change += 1
                osumEdge+=1
        print "after perturbing ,sum of odegree " + str(osumEdge) + "sum of idegree " + str(isumEdge)
        #从候选节点集中删除自己
        for anUserSet in userSet:
            u = self.getUser(anUserSet)
            candidate = u.candidateSim
            if u.ID in candidate:
                candidate.pop(u.ID)
            list1 = candidate.keys()
            u.setFistCandidateSorted(list1)
        return osumEdge