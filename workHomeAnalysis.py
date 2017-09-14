#-*- coding: UTF-8 -*-

import numpy as np  
import matplotlib.pyplot as plt 
from collections import namedtuple
from collections import defaultdict
from math import radians, cos, sin, asin, sqrt, atan2, pi ,radians, degrees
import matplotlib.cm as cm

#根据经纬度计算两点间距离，返回值单位为米 
def distance(lon1, lat1, lon2, lat2): # 经度1，纬度1，经度2，纬度2 （十进制度数）  
         
        # 将十进制度数转化为弧度  
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])  
      
        # haversine公式  
    dlon = lon2 - lon1   
    dlat = lat2 - lat1   
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2  
    c = 2 * asin(sqrt(a))   
    r = 6371 # 地球平均半径，单位为公里  
    return c * r * 1000

#求多个点的中心点坐标
def center_geolocation(geolocations):
    """
    Provide a relatively accurate center lat, lon returned as a list pair, given
    a list of list pairs.
    ex: in: geolocations = ((lon1,lat1), (lon2,lat2),)
        out: (center_lon,center_lat)
    """
    x = 0
    y = 0
    z = 0
    lenth = len(geolocations)
    for lon, lat in geolocations:
        lon = radians(float(lon))
        lat = radians(float(lat))
        
        x += cos(lat) * cos(lon)
        y += cos(lat) * sin(lon)
        z += sin(lat)

    x = float(x / lenth)
    y = float(y / lenth)
    z = float(z / lenth)

    return (degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y))))


# 读取一个用户的点，返回点的权重列表和点的归属时间列表
def readPoint(filename):
    
    fopen = open(filename, 'r')   
    Point = namedtuple('Point', ['x', 'y']) #创建Point对象
    pointSet = [] #存储该用户的所有的点
    dict_time = {}
    for eachLine in fopen:
        eachLine=eachLine.strip('\n') # 去掉每行的换行符
        pdata = eachLine.split(',')
        if pdata[2]=='' or pdata[3]=='':#有空的点则跳过
            continue
        pointSet.append([Point(pdata[2],pdata[3]),1])
        #统计work时间和home时间
        time = pdata[1][8:10]
        if 19<=int(time)<=24 or 0<=int(time)<=6:
            if Point(pdata[2],pdata[3]) in dict_time:
                dict_time[Point(pdata[2],pdata[3])].append('H')
            else:
                dict_time[Point(pdata[2],pdata[3])]=['H']
        elif 13<=int(time)<=17:
            if Point(pdata[2],pdata[3]) in dict_time:
                dict_time[Point(pdata[2],pdata[3])].append('W')
            else:
                dict_time[Point(pdata[2],pdata[3])]=['W']
        else:
            pass
      
    #计算点的权重
    data = defaultdict( int )
    for address ,value in pointSet:
        data[ address ] += value
    
    return data,dict_time

#聚类，返回点的聚类分组
def cluster(data,threshold):
    #print len(data)
    groupList = []
    #print data
    i=0
    while len(data)>0:
        i = i+1
        #print i
        group = []
        #选择权重最大的点作为leader
        for point, value in data.items():
            if value == max(data.values()):
                leader = point
                #print "leader"
                #print leader
               # data.pop(leader)#在点集合中移除leader                
        #计算点与leader的距离,如果小于阈值，则分为一组        
        for p in data.keys():
            #print distance(float(leader.x),float(leader.y),float(p.x),float(p.y))
            if distance(float(leader.x),float(leader.y),float(p.x),float(p.y))<threshold:                
                group.append(p)
                data.pop(p)
                #print data
        #print group
        if group:#如果该分组不为空，则添加到分组列表中
            groupList.append(group)
    return groupList

#画图将point点类展示在图中
def draw(pointGroup):
    color = ['b','g','r','c','m','y','k']
    k=0
    
    for point in pointGroup:
        x=[]
        y=[]        
        for p in point:
            x.append(float(p.x))
            y.append(float(p.y))
           
        plt.scatter(x, y, color=color[k])
        k = (k+1)%7
        
    plt.show()


#职住地提取
def home_workplace_detection(groupList,pointTime):
   
    group_weight=[]
    for group in groupList:
        home_work=[]
        for point in group:
            if point in pointTime:
                home_work.extend(pointTime[point])
        group_weight.append([home_work.count('H'),home_work.count('W')])

    print group_weight
    max_home = group_weight[0][0]
    max_work = group_weight[0][1]
    index_home = 0 #home最多的组号
    index_work = 0 #work最多的组号
    for i in range(len(group_weight)):
        if group_weight[i][0]> max_home:
            max_home = group_weight[i][0]
            index_home = i
        if group_weight[i][1]> max_work:
            max_work = group_weight[i][1]
            index_work = i
    
    return groupList[index_home],groupList[index_work]
    #home_work = [groupList[index_home]]+[groupList[index_work]]
    #返回家和工作地的分组    
    #return home_work
    
if __name__ == '__main__':
    filePath = "E:\\1000person\\015296844853261772.txt"
    print "---start---"
    pointWeight,pointTime = readPoint(filePath)
    #设置合适的阈值进行分组
    group = cluster(pointWeight,1000)
    #draw(group)
    home,work = home_workplace_detection(group,pointTime)
    #draw(home_work)
    print center_geolocation(home)
    print center_geolocation(work)

    print "---end---"
