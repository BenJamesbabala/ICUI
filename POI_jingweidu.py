# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:16:46 2019

@author: xin-yi.song
"""

import os
import csv
import time
import numpy as np
import pandas as pd

os.getcwd()
os.chdir(r"C:\Users\Xin-yi.Song\Desktop\ICUI\area")


name_list = []

with open('加油站_merge.csv', newline='',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

name_list = pd.DataFrame(name_list) 

#下列函数无法判断空值
#pd.isnull()
#pd.isna()
#只能直接用 if x 来判断

name_list['location']=name_list['location'].apply(lambda x: x if x else np.nan)#将空缺值标记为NAN
name_list.dropna(subset=['location'],inplace=True)#去掉含有NAN值的行
name_list.reset_index(drop = True,inplace=True)#去掉已经错位的index
name_list.drop(columns=['detail','street_id'],inplace=True)#去掉不需要的列
name_list.drop(name_list.columns[len(name_list.columns)-1], axis=1, inplace=True)#删除最后一列
#df.columns可以得到所有的列标签

start=time.clock()

for i, element in enumerate(name_list['location']):
    #print(i, element)
    #time.sleep(0.1)
    list_temp = element.split(',')
    print(i,list_temp)
    lat = list_temp[0]
    lng = list_temp[1]
    #print(i,lng)
    name_list.loc[i,'纬度'] = lat[8:len(lat)]#在表格中增加纬度
    name_list.loc[i,'经度'] = lng[8:len(lng)-1]#在表格中增加经度
    
elapsed=(time.clock()-start)
print("文件读入花费时间:",elapsed)
    
name_list['经度']=name_list['经度'].apply(lambda x: float(x) - 0.01185)
name_list['纬度']=name_list['纬度'].apply(lambda x: float(x) - 0.00328)

print(name_list)

name_list.to_csv('加油站_经纬度.csv',index = True,encoding = 'utf_8_sig')       





