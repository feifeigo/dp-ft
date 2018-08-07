# # -*- coding: utf-8 -*-
# class AttributeInfo:
#     member = []
#     perturb_Member = []
#     def __init__(self,name):
#         self.name = name
#         member = []
#         perturb_Member = []
#
#     def addMember(self,value):
#         self.member=list(self.member)
#         self.member.append(value)
#
#     def addPerMember(self,value):
#         self.perturb_Member=list(self.perturb_Member)
#         self.perturb_Member.append(value)
#
#     def setNum_member(self):
#         self.num_member = self.member.__len__()
#
#     def setNum_perturbmember(self):
#         self.num_perturb = self.perturb_Member.__len__()
#
#     def setLink_member(self,value):
#         self.link_member=value
#
#     def setPserLink_member(self,value):
#         self.perturb_link_member =value
#
#     def getNum_member(self):
#         return self.member.__len__()
#
#     def setCodfficent(self,value):
#         if self.getNum_member()>1:
#             self.coefficent = value/((self.getNum_member() - 1.0) * self.getNum_member())
#         else:
#             self.coefficent=0
#     def setPerCoefficent(self,value):
#         size = self.perturb_Member.__len__()
#         if size>1:
#             self.perCoefficent = value/((size - 1.0) * size)
#         else:
#             self.perCoefficent =0
#         print "perCoefficent",self.perCoefficent
#
#     def toString(self):
#         s = self.name+"聚集系数" + str(self.coefficent)
#         return s
