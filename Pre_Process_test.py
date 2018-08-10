# -*- coding: utf-8 -*-


from AttributeInfo import *
from AttributeList import *
from FileUtil import *
from UserList import *
from UserInfo import *
from numpy import *
import string
from Queue import *
from random import *
from SimCompute import *
global DATASET_DIR
DATASET_DIR="D:/IDEA/DP-FTexperiment/dataSets/"
global RESULT_DIR
RESULT_DIR="D:/aaaapytest/"


if __name__ == "__main__":
    sc = SimCompute()
    # dataSet = raw_input("输入数据集名称：")
    dataSet ='jazz'
    # /&\区别
    DATASET_PATH = DATASET_DIR + dataSet
    RESULT_PATH=RESULT_DIR + dataSet
    # print "原始数据集路径："+DATASET_PATH
    # privately = raw_input("是否进行差分隐私扰动？(是-1/否-0)：")
    # directer = raw_input("是否为有向图？(是-1/否-0)：")

    nattribute = 0
    epsilon1 = 0.0
    privately = '0'
    directer = '0'

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
        # sc.ge1UDLink(output_dir, dataSet)
        sc.generateUDLink(output_dir, dataSet)

    # def random_pick(some_list, probabilities):
    #     x = random.uniform(0,1)
    #     cumulative_probability = 0.0
    #     for item, item_probability in zip(some_list, probabilities):
    #         cumulative_probability += item_probability
    #         if x < cumulative_probability: break
    #     return item
    #
    # def test_random(nu):
    #     a = [1, 2, 3, 4]
    #     b = [0.00001, 0.000022, 0.3, 0.698978]
    #     re = dict(zip(a, [0] * 4))
    #     for x in xrange(nu):
    #         result = random_pick(a, b)
    #         re[result] += 1
    #     for v, value in re.iteritems():
    #         re[v] = float(value) / nu
    #     return re
    # re = test_random(10000000)
    # print re
    # for i in re:
    #     print i,"+",re[i]/re[1]


    # que = Queue.Queue()
    # que.put(2)
    # print que
    # print que.qsize()
    # if que.empty():
    #     print 1
    # else:
    #     print que.get()

    # li=[1,2,3,4,5]
    # a = random.choice(li)
    # print a

    # q=Queue.Queue()
    # A=0
    # q.put(5)
    # q.put(5)
    # B=0
    # q.put(5)
    # q.put(5)
    # print "que size",q
    # for i in range(q.qsize()):
    #     a = q.get()
    #     print a




