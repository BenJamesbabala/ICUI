# -*- coding: utf-8 -*-
"""
Created on Fri May 10 15:18:14 2019

@author: xin-yi.song
"""
import os
import csv
import time 
import numpy as np
import pandas as pd

os.getcwd()
os.chdir(r"C:\Users\xinyisong\Desktop\ICUI\POLLUTION_2")

############################读取大表格#########################################
name_list = []
with open('监测点信息汇总_新_3000.csv', newline='',encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

info = pd.DataFrame(name_list) 

#for j in range(0,info.shape[1]):#将空缺值标记为0
    #info.iloc[:,j]=info.iloc[:,j].apply(lambda x: x if x else 0)
###########################日数据##############################################    
name_list = []
with open('日数据.csv', newline='',encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

dd = pd.DataFrame(name_list)
dd=pd.merge(dd,info,how='left',on=['点位名称'])

dd = dd.dropna()
dd.drop(dd.columns[0],axis=1,inplace=True)
#dd.reset_index(drop = True,inplace=True)#去掉多余的index

dd.to_csv('日数据汇总.csv',index = False,encoding = 'utf_8_sig')   

###########################周数据##############################################    
name_list = []
with open('周数据.csv', newline='',encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

ww = pd.DataFrame(name_list)
ww=pd.merge(ww,info,how='left',on=['点位名称'])

ww = ww.dropna()
ww.drop(ww.columns[0],axis=1,inplace=True)
#dd.reset_index(drop = True,inplace=True)#去掉多余的index

ww.to_csv('周数据汇总.csv',index = False,encoding = 'utf_8_sig')   
#############################月数据#############################################
name_list = []
with open('月数据.csv', newline='',encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

mm = pd.DataFrame(name_list)
mm=pd.merge(mm,info,how='left',on=['点位名称'])
mm = mm.dropna()
mm.drop(mm.columns[0],axis=1,inplace=True)

mm.to_csv('月数据汇总.csv',index = False,encoding = 'utf_8_sig')   