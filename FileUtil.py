# -*- coding: utf-8 -*-
import os
class FileUtil:
    def createFile(self,destFileName):
        # 文件已存在
        if os.path.isfile(destFileName):
            print "创建单个文件" + destFileName + "失败，目标文件已存在,准备删除重建！"
            os.remove(destFileName)
        #路径非目录
        if os.path.isdir(destFileName):
            print "创建单个文件" + destFileName + "失败，目标文件不能为目录！"
            return False
        #判断目标文件所在的目录是否存在
        if not os.path.exists(os.path.dirname(destFileName)):
            print "目标文件所在目录不存在，准备创建它！"
            os.makedirs(os.path.dirname(destFileName))
            if not os.path.exists(os.path.dirname(destFileName)):
                print "创建目标文件所在目录失败！"
                return False
        # 创建目标文件
        if open(destFileName, 'w'):
            print "创建单个文件" + destFileName + "成功！"
            return True
        else:
            print "创建单个文件" + destFileName + "失败！"
            return False

    def writeTextFile(self,fileName,set):
        self.createFile(fileName)
        fp = open(fileName, 'w')
        print "开始创建"+fileName
        for i in range(len(set)):
            fp.write(str(set[i])+'\n')
        print "创建完毕" + fileName
        fp.close()

