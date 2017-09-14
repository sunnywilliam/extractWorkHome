#-*- coding: UTF-8 -*-

import os

dict_person={}
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
    print ("reading %s"%(filename))
    f = open(filename, 'r') # r 代表read
    s = f.read()
    lines=s.split('\n')
    for eachLine in lines:
        data = eachLine.split(',')
        if data[0] in dict_person:
            dict_person[data[0]].append([data[0],data[2],data[4],data[5]])
        else:
            if(len(dict_person)<=1000):
                dict_person[data[0]]=[[data[0],data[2],data[4],data[5]]]


if __name__ == '__main__':
    global location
    filePath = "E:\\data\\"
    print "---start---"
    #遍历2级目录
    for i in eachFile(filePath)[0:7]:# 只选择一周的文件
        i = i+"\\"+os.path.basename(i) #两层文件夹添加
        for j in eachFile(i+"\\"):
            if len(os.path.basename(j)) == 16: #除去记录时间的文件
                readFile(j)
            
    #根据人员编号创建文件
    for user in dict_person.keys():
        pfilename = "E:\\1000person\\"+user+".txt"
        fb = open(pfilename,'a')
        for userdata in dict_person[user]:
            for each in userdata:
                fb.write(each+",")
            fb.write("\n")
            
    print "---end---"
