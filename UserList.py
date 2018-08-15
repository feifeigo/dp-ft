# -*- coding: utf-8 -*-
from numpy import *
from math import *
import string
import sys as sys
import gc as gc
import time as time

class UserList:
    alpha = float(0.75)
    # IN_DEGREE = 1
    # OUT_DEGREE = 2
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

    # def count_n_hop_neighbor(self,u,hop):
    #     for i in range(1,hop):
    #         for i in u.AllHip1User():
    #             u.n_hop_neighbor=list(set(u.n_hop_neighbor).union(set(self.getUser(i).AllHip1User())))

    # initialazation. includes: 1-step correlation and random walk
    def initUserInfo(self,perturb,epsilon):
        userSet = self.AllUser()#排序后userset
        ousumEdge = 0
        insumEdge = 0
        # 计算入度和出度和
        for ID in userSet:
            u = self.getUser(ID)
            u.setDegree()#设置了out_degree和in_dgree（原图）
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
            # 初始化temp,msim
            u.tempSim = dict(u.candidateSim)
            u.msimSim = dict(u.candidateSim)
        print "the initialzation of corelation transition probability finished"
        numofv=userSet.__len__()
        osumEdge = 0
        isumEdge = 0
        # call random walk correlation computation, you can change the walk_step
        # 差分扰动
        for anUserSet in userSet:
            u = self.getUser(anUserSet)
            # 为节点施加度差分隐私保护
            u.setPeDegree(perturb, epsilon,numofv)
            osumEdge += u.getODegree()
            isumEdge += u.getIDegree()
        print "lrw begins "
        time_start= time.time()
        # LRW
        for i in range(1, self.walk_step):
            print "loop",i,"begins"
            last = time.time()
            d = {}
            ilrw=1
            for uid in userSet:
                ui = self.getUser(uid)
                dic={}
                for ujd in userSet:
                    uj = self.getUser(ujd)
                    se = list(set(ui.tempSim.keys()) | set(uj.tempSim.keys()))
                    tem=0
                    for ukd in se:
                        uk = self.getUser(ukd)
                        tem += ui.get_temp(ukd)*uk.get1_simValue(ujd)
                    dic[ujd]=tem
                d[uid]=dic
                if ilrw % 1000 == 0:
                    print "no.", ilrw, "node finised lrw"
                    now=time.time()
                    print "this period costs",now-last
                ilrw += 1
            print "lrw finished in loop ",i ,",begin to update temp&msim"
            #     游走一次结束后统一更新temp和msim
            for uid in d.keys():
                ui = self.getUser(uid)
                for i in d[uid].keys():
                    ui.tempSim[i]=d[uid].get(i)
                    if i in ui.msimSim.keys():
                        ui.msimSim[i] = ui.msimSim[i] + ui.tempSim.get(i)
                    else:
                        ui.msimSim[i] = ui.tempSim.get(i)
                # print "u",uid, ui.msimSim
                # print ui.tempSim
        time_end = time.time()
        print'totally cost', time_end - time_start
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
        #计算吸引力
        for anUserSet in userSet:
            u = self.getUser(anUserSet)
            for ujd in u.msimSim:
                u.add_wei(ujd, math.pow(u.msimSim.get(ujd), self.index) * self.getUser(ujd).i_degree)
                # print "ujd",ujd, "weight",math.pow(u.msimSim.get(ujd), self.index) * self.getUser(ujd).i_degree
        #从候选节点集中删除自己
        for anUserSet in userSet:
            u = self.getUser(anUserSet)
            candidate = u.candidateSim
            if u.ID in candidate:
                candidate.pop(u.ID)
            list1 = candidate.keys()
            u.setFistCandidateSorted(list1)
        return osumEdge