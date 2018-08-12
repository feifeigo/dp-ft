# -*- coding: utf-8 -*-
import random
from numpy import *

# 产生一个float型的随机数，判断每个候选集用户出现的概率
# 返回值ran：candidate列表中的序列（candidates中的第ran个就是抽中的用户）
class FtSample:

    def getPrizeIndex(self,firstCandidateSorted,candidates):
        ran=0
        # 计算总权重
        sumWeight = 0.0
        for i in range(len(firstCandidateSorted)):
            sumWeight+=candidates.get(firstCandidateSorted[i])
        # 产生随机数
        randomNumber = round(random.random(), 2)
        d1=0.0
        d2=0.0
        for i in range(len(firstCandidateSorted)):
            if sumWeight==0.0:
                dt2=float('inf')
            else:
                d2+=candidates.get(firstCandidateSorted[i])/sumWeight
            if i==0:
                d1=0
            else:
                if sumWeight == 0.0:
                    dt2 = float('inf')
                else:
                    d1+=candidates.get(firstCandidateSorted[i-1])/sumWeight
            if randomNumber >=d1 and randomNumber<=d2 :
                ran=i
                break
        return ran



