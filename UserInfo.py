# -*- coding: utf-8 -*-
from AttributeInfo import *
import math
import random
from decimal import *

class UserInfo:
    degree_sensitivity = 2
    numOfAff_sensitivity = 2


    def __init__(self,ID,position):
        self.ID = ID
        self.position = position
        self.o_degree = 0.0#扰动后出入度
        self.i_degree = 0.0
        self.out_degree=0#原图出入度
        self.in_degree=0
        self.adjOutList = []#出度邻点集
        self.adjInList = []#入度邻点集
        self.Affiliation = []
        self.Prob_Affiliation = []
        self.firstCandidateSorted = []#候选节点集
        # self.secondCandidateSorted = []
        self.candidateSim = {}#节点间的相关度、吸引力
        self.Prob_AdjList = []#已成边节点集
        self.ID1select=False#是否选中为ID1
        self.IDnselect=False#是否选中为IDn

    def setID1select(self,bool):
        self.ID1select = bool

    def setIDnselect(self,bool):
        self.IDnselect = bool

    def getID1select(self):
        return self.ID1select

    def getIDnselect(self):
        return self.IDnselect

    def get1_simValue(self,key):
        if self.candidateSim.get(key)==None:
            return 0.0
        else:
            return self.candidateSim.get(key)

    def add_Sim(self, key, value):
        self.candidateSim[key]=value

    def setPeDegree(self,perturb,epsilon1):
        odegree = self.out_degree
        idegree = self.in_degree
        if perturb=='1':
            # 为节点施加度差分隐私保护
            odegree += self.differiencialNoise(self.degree_sensitivity, epsilon1)
            idegree += self.differiencialNoise(self.degree_sensitivity, epsilon1)
            while ((odegree < 0) or(idegree < 0)or ((odegree == 0) and (idegree == 0)) or(odegree > len(self.candidateSim)) or (idegree > len(self.candidateSim))) :
                odegree = self.out_degree + self.differiencialNoise(self.degree_sensitivity, epsilon1)
                idegree = self.in_degree + self.differiencialNoise(self.degree_sensitivity, epsilon1)
        self.o_degree = odegree
        self.i_degree = idegree

    def setNumOfAff(self):
        self.numOfAff = self.Affiliation.__len__()

    def setPerNumOfAff(self, epsilon2):
        print self.Affiliation
        num = self.Affiliation.__len__() + self.differiencialNoise(self.numOfAff_sensitivity, epsilon2)
        while ((num < math.sqrt(self.Affiliation.__len__())) or (num > 4 * self.Affiliation.__len__())):
            num = self.Affiliation.__len__() + self.differiencialNoise(self.numOfAff_sensitivity, epsilon2)
        self.numOfPerAff = num

    def getODegree(self):
        return self.o_degree

    def getIDegree(self):
        return  self.i_degree

    def setFistCandidateSorted(self, list):
        self.firstCandidateSorted = list

    def toString(self):
        print "ID:" + self.ID + "位置：" + self.position + ";出度： " + self.getODegree()  + ";入度：" + self.getIDegree()

    def AttributeToString(self):
        N =self.ID
        for s in self.Affiliation:
            N+=" "+s
        return N

    def PerAttributeToString(self):
        N = self.ID
        for s in self.Prob_Affiliation:
            N += " " + s
        return N

    def AllHip1User(self):
        lt = list(set(self.adjInList).union(set(self.adjOutList)))
        # lt.sort()#/////////////////////////////////////////////////////////////////////////////////////////////////////
        return lt

    def addAdjOut(self,value):
        self.adjOutList.append(value)

    def getPerAffSize(self):
        return self.Prob_Affiliation.__len__()

    def addAdjIn(self,value):
        self.adjInList.append(value)

    def addAttri(self,value):
        self.Affiliation.append(value)

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







