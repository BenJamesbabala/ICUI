﻿# -*- coding: utf-8 -*-
"""
Created on Thu May  2 13:47:49 2019

@author: xin-yi.song
"""

import time
import json
from urllib.request import urlopen
import urllib 
import pandas as pd


url0=r"http://api.map.baidu.com/place/v2/search?"
ak=r"&ak=x1kbYRksKTuBGRa0EXGgIB55cL6WqNSL"
#ak=r"&ak=KaFVoxkG7bso7QlDUY8w5tuZG1LG33tq"
#ak=r"&ak=5UK6Um2nRBqID8cTTgYblTbGQREW8DtC"

POI="公交站"
POI=urllib.parse.quote(POI.encode('utf-8'))
#4种POI：饭店、工厂、公交站、加油站
#一级行业分类  二级行业分类
#  美食           中餐厅
#  交通设施       公交车站，加油加气站
 
left_bottom = [120.861562,30.661087] # 设置区域左下角坐标（百度坐标系）
right_top = [122.029708,31.564006] # 设置区域右上角坐标（百度坐标系）

x_number = 15
y_number = 15

x_item = (right_top[0]-left_bottom[0])/x_number
y_item = (right_top[1]-left_bottom[1])/y_number

n = 0 #切片计数器
nametable = []

#'address','area','city','detail','location','name','province','street_id','telephone' ,'uid']

for i in range(10,15):
    for j in range(y_number):
        left_bottom_part = [left_bottom[0]+i*x_item,left_bottom[1]+j*y_item]; # 切片的左下角坐标
        right_top_part = [left_bottom_part[0]+x_item,left_bottom_part[1]+y_item]; # 切片的右上角坐标
        
        for k in range(20):
            url= url0 + 'query=' + POI + '&page_size=20&page_num=' + str(k) + '&scope=1' + '&bounds=' + str(left_bottom_part[1]) + ',' + str(left_bottom_part[0]) + ','+str(right_top_part[1]) + ',' + str(right_top_part[0]) + '&output=json' + ak     
            #http://api.map.baidu.com/place/v2/search?query=美食&page_size=10&page_num=0&scope=1&bounds=39.915,116.404,39.975,116.414&output=json&ak={您的密钥}
            #scope:检索结果详细程度。取值为1 或空，则返回基本信息；取值为2，返回检索POI详细信息   
            res=urlopen(url)
            cet=res.read()
            result=json.loads(cet)
            #print(result)
            #time.sleep(1)
            
            names = result['results']
            #names = pd.DataFrame(names)
            print(names)
            nametable.extend(names)
            
            
        n += 1;
        print( '第',str(n),'个切片入库成功')

nametable = pd.DataFrame(nametable)
nametable.to_csv(r'C:\Users\xinyisong\Desktop\ICUI\area\公交站_225.csv',index = True,encoding = 'utf_8_sig')         




    