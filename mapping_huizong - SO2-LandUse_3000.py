# -*- coding: utf-8 -*-
"""
Created on Tue May  7 19:47:03 2019

@author: xin-yi.song
"""

import os
import csv
import glob
import numpy as np
import pandas as pd

os.getcwd()
os.chdir(r"C:\Users\xinyisong\Desktop\ICUI\mapping\mapping_数据库")

files=glob.glob('*.txt')

####################################读取大表格###################################
name_list = []
with open(r'网格点信息表_temp.csv', newline='',encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

result = pd.DataFrame(name_list) 

for j in range(0,result.shape[1]):#将空标记为nan
    result.iloc[:,j]=result.iloc[:,j].apply(lambda x: x if x else np.nan)

df = result
##################################污染物#####################################
line_list = []

with open("二氧化硫.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp)

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
data = pd.DataFrame(line_list,columns=heads)  
data.rename(columns={'RASTERVALU\r\n':'二氧化硫'}, inplace=True)

for j in range(0,data.shape[1]):#将换行符标记为nan
    data.iloc[:,j]=data.iloc[:,j].apply(lambda x: np.nan if x=='\r\n' else x)


data['二氧化硫'] = pd.to_numeric(data['二氧化硫']) 
data['二氧化硫']=data['二氧化硫'].apply(lambda x: np.nan if x<0 else x)
data.fillna(data.mean()['二氧化硫'],inplace=True)#用平均值替代缺失值
data = data[['LON','LAT','二氧化硫']]

df=pd.merge(df,data,how='left',on=['LAT'])
df.rename(columns={'LON_x':'LON'}, inplace=True)
df.drop(columns=['LON_y'],inplace=True)

info=df.describe()

####################################土地利用###################################
line_list = []

with open("居住_3000.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split('\t')
        line_temp[2]=line_temp[2].rstrip('\r\n')
        line_list.append(line_temp)
        
heads = ['LON','LAT','居住_3000']
data = pd.DataFrame(line_list,columns=heads) 

data['居住_3000'] = pd.to_numeric(data['居住_3000']) 
data['居住_3000']=data['居住_3000'].apply(lambda x: x if x else np.nan)
#data.fillna(data.mean()['水域_3000'],inplace=True)#用平均值替代缺失值
data.describe()

df=pd.merge(df,data,how='left',on=['LON','LAT'])
#df.drop(columns=['水域_3000'],inplace=True)

####################################导出######################################
df.to_csv('网格点信息汇总.csv',index = False,encoding = 'utf_8_sig') 