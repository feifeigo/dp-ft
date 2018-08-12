# -*- coding: utf-8 -*-
import os
class FileUtil:
    def createFile(self,destFileName):
        # 文件已存在
        if os.path.isfile(destFileName):
            print "creating " + destFileName + " failed，it already exists,now delete it "
            os.remove(destFileName)
        #路径非目录
        if os.path.isdir(destFileName):
            print "creating " + destFileName + " failed，it can't be a directory "
            return False
        #判断目标文件所在的目录是否存在
        if not os.path.exists(os.path.dirname(destFileName)):
            print "the directory doesn't exists，now create it "
            os.makedirs(os.path.dirname(destFileName))
            if not os.path.exists(os.path.dirname(destFileName)):
                print "creating directory failed "
                return False
        # 创建目标文件
        if open(destFileName, 'w'):
            print "creating the file " + destFileName + " finished "
            return True
        else:
            print "creating the file " + destFileName + " failed "
            return False

    def writeTextFile(self,fileName,set):
        self.createFile(fileName)
        fp = open(fileName, 'w')
        print "begin writing "+fileName
        for i in range(len(set)):
            fp.write(str(set[i])+'\n')
        print "finished writting " + fileName
        fp.close()

