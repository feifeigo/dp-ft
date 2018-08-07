# -*- coding: utf-8 -*-
from numpy import *
from math import *
import string

class UserList:
    alpha = float(0.75)
    IN_DEGREE = 1
    OUT_DEGREE = 2
    index = 3 #index 对应于论文中公式2-9的伽马
    walk_step = 4

    def __init__(self):
        self.userList = {}

    def AllUser(self):
        lt = self.userList.keys()
        # lt.sort(key=lambda x: string.atoi(x), reverse=False)#///////////////////////////////////排序浪费时间//////////////////////////////////////////////////////////////////////
        return lt

    def setUserList(self,userList):
        self.userList = userList

    def getUser(self,id):
        return self.userList.get(id)

    def addUser(self, key, value):
        self.userList[key]=value

    def getFirstNodeID(self,list):
        if list:
            return list[0]
        else:
            return None

#     def createUserList(self,fileName):
#         print "createUserList has not finished"
#     def createAttribute(self,fileName):
#         print "createAttribute has not finished"
#     def createAdjMember(self,fileName,directer):
#         print "createAdjMember has not finished"
    def count_n_hop_neighbor(self,n_hop_neighbor,u,hop):
        for i in range(1,hop):
            for i in u.AllHip1User():
                n_hop_neighbor=list(set(n_hop_neighbor).union(set(self.getUser(i).AllHip1User())))
        # n_hop_neighbor.sort()/////////////////////////////////////////////////////////////////////////////////
        return n_hop_neighbor

    def mmltiple(self,a,b):
        result = mat(zeros((a.__len__(), b[0].__len__())))
        for i in range(a.__len__()):
            result=a*b
        return result

    # 二维矩阵相加
    def add(self,a,b):
        result = mat(zeros((a.__len__(),b[0].__len__())))
        result = a+b
        return result

    def LRW(self,u):
        n_hop_neighbor = []
        for i in u.AllHip1User():
            n_hop_neighbor.append(i)
        n_hop_neighbor=self.count_n_hop_neighbor(n_hop_neighbor,u,self.walk_step)
        seq2id = {}
        id2seq = {}
        seq = 0
        for user in n_hop_neighbor:
            seq2id[seq] = user
            id2seq[user] = seq
            seq+=1
        n_hop_neighbor_size = n_hop_neighbor.__len__()
        tempMatrix = mat(zeros((n_hop_neighbor_size,n_hop_neighbor_size)))
        simMatrix = mat(zeros((n_hop_neighbor_size,n_hop_neighbor_size)))#相关度矩阵
        transMatrix = mat(eye(n_hop_neighbor_size,n_hop_neighbor_size,dtype=int))
        # 采用一步转移概率矩阵作为社交网络节点间的初始相关度矩阵
        for i in range(0,n_hop_neighbor_size):
            for j in range(0,n_hop_neighbor_size):
                if seq2id.get(j) in (self.getUser(seq2id.get(i))).AllHip1User():
                    transMatrix[i, j]=self.getUser(seq2id.get(i)).get1_simValue(seq2id.get(j))
                else:
                    pass
        simMatrix = self.add(simMatrix, transMatrix)
        # 随机游走
        for i in range(1,self.walk_step):
            tempMatrix = self.mmltiple(simMatrix, transMatrix)
            simMatrix = self.add(simMatrix, tempMatrix)
        target_user_seq = id2seq.get(u.ID)
        for sequence in range(n_hop_neighbor_size):
            v_id=seq2id.get(sequence)
            sim_uv= simMatrix[target_user_seq,sequence]
            v=self.getUser(v_id)
            # force compute
            weight=math.pow(sim_uv, self.index) * v.getIDegree()
            # save the corelation
            # 保存节点间相关度
            u.add_Sim(v_id, weight)

    # initialazation. includes: 1-step correlation and random walk
    def initUserInfo(self,perturb,epsilon):
        userSet = self.AllUser()#排序后userset
        ousumEdge = 0
        insumEdge = 0
        # 计算入度和出度和
        for ID in userSet:
            u = self.getUser(ID)
            u.setDegree()
            # 属性相关用不上
            # u.setNumOfAff()
            ousumEdge += u.getOutDegree()
            insumEdge += u.getInDegree()
        print "出度和" , ousumEdge , "入度和" , insumEdge
        # 为每个用户初始化one - hop相关度
        for anUserSet in userSet:
            sum = 0.0
            u = self.getUser(anUserSet)
            if u.adjInList:
                for a in u.adjInList:
                    sim_ku = (1.0 - self.alpha) / u.in_degree
                    u.add_Sim(a, (u.get1_simValue(a) + sim_ku))
            if u.adjOutList:
                for a in u.adjOutList:
                    sim_ku = float(self.alpha / u.out_degree) + (1.0 - self.alpha)
                    u.add_Sim(a, (u.get1_simValue(a) + sim_ku))
            for a in u.candidateSim.keys():
                sum += u.candidateSim.get(a)
            if not sum == 0.0:
                for a in u.candidateSim.keys():
                    value = u.candidateSim.get(a)
                    # 初始化相关度归一化处理
                    u.add_Sim(a, (value / sum))
        print "候选节点集相关度初始化成功！"

        osumEdge = 0
        isumEdge = 0
        # call random walk correlation computation, you can change the walk_step
        for anUserSet in userSet:
            u = self.getUser(anUserSet)
            # 基于LRW的节点间相关度计算
            self.LRW(u)
            # 为节点施加度差分隐私保护
            u.setPeDegree(perturb, epsilon)
            osumEdge += u.getODegree()
            isumEdge += u.getIDegree()
        print "差分隐私扰动后：出度和" + str(osumEdge) + "入度和" + str(isumEdge)

        for anUserSet in userSet:
            u = self.getUser(anUserSet)
            candidate = u.candidateSim
            if u.ID in candidate:
                candidate.pop(u.ID)
            list1 = candidate.keys()
            u.setFistCandidateSorted(list1)
        return osumEdge