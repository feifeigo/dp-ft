# # -*- coding: utf-8 -*-
# from AttributeInfo import *
# class AttributeList:
#     # attributeList = {}
#
#     def __init__(self):
#         self.attributeList = {}
#
#     def Size(self):
#         return self.attributeList.__len__()
#
#     # 获得所有属性的排序后列表
#     def Allattribute(self):
#         # self.attributeList = dict(self.attributeList)
#         lt = self.attributeList.keys()
#         # print "before sort list",list
#         lt.sort(key=lambda x: self.attributeList.get(x).getNum_member(), reverse=False)
#         return lt
#
#     def getGroup(self,key):
#         return self.attributeList.get(key)
#
#     def addGroup(self,key,value):
#         self.attributeList = dict(self.attributeList)
#         self.attributeList[key]=value
#
#     def createAttList(self,fileName):
#     #
#         print "createAttList has not finished"
#
#     def createMember(self,fileName):
#         print "createMember has not finished"