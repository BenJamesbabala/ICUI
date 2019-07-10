# -*- coding: utf-8 -*-
"""
Created on Sat May  4 10:49:57 2019

@author: xinyisong
"""

import os
import csv
import time
import pandas as pd

os.getcwd()
os.chdir("C:/Users/xinyisong/Desktop/ICUI/area")

start=time.clock()

name_list = []

with open('加油站_75.csv', newline='',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row['name'], row['province'], row['city'], row['area'], row['address'], row['location'],row['uid'])
        row = dict(row)
        #print(row)
        name_list.append(row)
        
with open('加油站_150.csv', newline='',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row = dict(row)
        name_list.append(row)
        
with open('加油站_225.csv', newline='',encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        row = dict(row)
        name_list.append(row)     
        
name_list = pd.DataFrame(name_list)           
print(name_list)
        
elapsed=(time.clock()-start)
print("文件读入花费时间:",elapsed)

name_list.to_csv('加油站_merge.csv',index = True,encoding = 'utf_8_sig')         