# -*- coding: utf-8 -*-
import math
import random
from decimal import *

class UserInfo:
    degree_sensitivity = 2
    numOfAff_sensitivity = 2
    __slots__ = ['ID', 'position','o_degree', 'i_degree','out_degree','in_degree','adjOutList','adjInList','firstCandidateSorted','candidateSim','weight','corela','Prob_AdjList','n_hop_neighbor']

    def __init__(self,ID,position):
        self.ID = ID
        self.position = position
        self.o_degree = 0.0#扰动后出入度
        self.i_degree = 0.0
        self.out_degree=0#原图出入度
        self.in_degree=0
        self.adjOutList = []#出度邻点集
        self.adjInList = []#入度邻点集
        self.firstCandidateSorted = []#候选节点集
        self.candidateSim = {}#前期存放初始概率
        self.weight = {}#吸引力
        self.corela={}#存放矩阵运算后的节点间相关度
        self.Prob_AdjList = []#已成边节点集
        self.n_hop_neighbor=[]#n步游走后邻点集

    def get1_simValue(self,key):
        if self.candidateSim.get(key)==None:
            return 0.0
        else:
            return self.candidateSim.get(key)

    def add_Sim(self, key, value):
        self.candidateSim[key]=value

    def add_wei(self, key, value):
        self.weight[key]=value

    def add_Cor(self, key, value):
        self.corela[key]=value

    def setPeDegree(self,perturb,epsilon1,numofv):
        odegree = self.out_degree
        idegree = self.in_degree
        if perturb=='1':
            # 为节点施加度差分隐私保护
            odegree += self.differiencialNoise(self.degree_sensitivity, epsilon1)
            idegree += self.differiencialNoise(self.degree_sensitivity, epsilon1)
            while ((odegree < 0) or(idegree < 0)or ((odegree == 0) and (idegree == 0)) or(odegree > len(self.candidateSim)) or (idegree > len(self.candidateSim)) or (idegree> numofv-2) or (odegree>numofv-2)) :
                odegree = self.out_degree + self.differiencialNoise(self.degree_sensitivity, epsilon1)
                idegree = self.in_degree + self.differiencialNoise(self.degree_sensitivity, epsilon1)
            odegree = 1 if (1>odegree ) else odegree
            idegree = 1 if (1>idegree) else idegree
            odegree = numofv if (numofv<odegree) else odegree
            idegree = numofv if (numofv<idegree) else idegree
        self.o_degree = odegree
        self.i_degree = idegree

    def getODegree(self):
        return self.o_degree

    def getIDegree(self):
        return  self.i_degree

    def setFistCandidateSorted(self, list):
        self.firstCandidateSorted = list

    def AllHip1User(self):
        lt = list(set(self.adjInList).union(set(self.adjOutList)))
        return lt

    def addAdjOut(self,value):
        self.adjOutList.append(value)

    def addAdjIn(self,value):
        self.adjInList.append(value)

    def setDegree(self):
        self.out_degree = len(self.adjOutList)
        self.in_degree = self.adjInList.__len__()

    def getOutDegree(self):
        return self.out_degree

    def getInDegree(self):
        return self.in_degree

    def differiencialNoise(self,sensitivity,epsilon):
        uniformDistributionVar = random.random()
        if uniformDistributionVar==0:
            noise = Decimal('-Inf')
        elif 0<uniformDistributionVar and uniformDistributionVar<0.5:
            noise = Decimal(sensitivity/epsilon*math.log(2*uniformDistributionVar))
        else:
            noise =Decimal(-sensitivity/epsilon*math.log(2-2*uniformDistributionVar))
        noise = noise.quantize(Decimal('1'), ROUND_HALF_DOWN)

        return  int(noise)







