# -*- coding: utf-8 -*-


from AttributeInfo import *
from AttributeList import *
from FileUtil import *
from UserList import *
from UserInfo import *
from numpy import *
import string
from SimCompute import *
global DATASET_DIR
DATASET_DIR="D:/IDEA/DP-FTexperiment/dataSets/"
global RESULT_DIR
RESULT_DIR="D:/aaaapytest/"


if __name__ == "__main__":
    sc = SimCompute()
    # dataSet = raw_input("输入数据集名称：")
    dataSet ='little'
    # /&\区别
    DATASET_PATH = DATASET_DIR + dataSet
    RESULT_PATH=RESULT_DIR + dataSet
    # print "原始数据集路径："+DATASET_PATH
    # privately = raw_input("是否进行差分隐私扰动？(是-1/否-0)：")
    # directer = raw_input("是否为有向图？(是-1/否-0)：")

    nattribute = 0
    epsilon1 = 0.0
    privately = '0'
    directer = '1'

    if privately=='1':
        # epsilon1 = input("请输入社交关系隐私预算：")
        epsilon1 = 2
        print "社交关系隐私预算：",epsilon1
        epsilon2 = 0.0
        # 初始化过程，包含差分隐私扰动
        sc.preProcess(DATASET_PATH,privately,directer,epsilon1)
        # withAttr 属性处理略
    else:
        # 初始化过程，不包含差分隐私扰动
        sc.preProcess(DATASET_PATH, privately, directer, epsilon1)
    output_dir = RESULT_PATH +"/nattributes_" + str(nattribute) + "/FT_" + str(epsilon1)
    print output_dir
    if directer=='1':
    #     有向图
        sc.generateDLink(output_dir, dataSet)
    else:
        sc.generateUDLink(output_dir, dataSet)

