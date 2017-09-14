#-*- coding: UTF-8 -*-
import os

# 遍历指定目录，返回目录下的所有文件名
def eachFile(filepath):
    pathDir =  os.listdir(filepath)
    child = []
    for allDir in pathDir:
        child.append(os.path.join('%s%s' % (filepath, allDir)))
    return child
    #print child.decode('gbk') # .decode('gbk')是解决中文显示乱码问题

# 读取文件内容并按用户ID写入文件
def readFile(filename):
    fopen = open(filename, 'r') # r 代表read
    for eachLine in fopen:
       data = eachLine.split(',')
       #根据人员编号创建文件
       pfilename = 'E:\\user\\'+data[0]+".txt"
       fb = open(pfilename,'a')
       aLine = data[0]+","+data[2]+","+data[4]+","+data[5]+"\n"
       fb.write(aLine)
    fopen.close()
    fb.close()
    

if __name__ == '__main__':
    filePath = "E:\\data\\"
    print "---start---"
    #遍历2级目录
    for i in eachFile(filePath):
        i = i+"\\"+os.path.basename(i) #两层文件夹添加
        for j in eachFile(i+"\\"):
            if len(os.path.basename(j)) == 16: #除去记录时间的文件
                readFile(j)
    print "---end---"
  
