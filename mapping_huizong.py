# -*- coding: utf-8 -*-
"""
Created on Tue May  7 19:47:03 2019

@author: xin-yi.song
"""

import os
import glob
import numpy as np
import pandas as pd

os.getcwd()
os.chdir(r"C:\Users\xin-yi.song\Desktop\ICUI\mapping\mapping-数据库")

files=glob.glob('*.txt')

################################读取点位信息#####################################
line_list = []

with open("监测点.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp)

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
df = pd.DataFrame(line_list,columns=heads)  
df.rename(columns={'NEAR_DIST\r\n':'离海的距离（米）'}, inplace=True)#修改列名
#df['LON'] = pd.to_numeric(df['LON']) 
#df['LAT'] = pd.to_numeric(df['LAT']) 
df['离海的距离（米）'] = pd.to_numeric(df['离海的距离（米）']) 

df = df[['LON','LAT','离海的距离（米）']]

################################个数#######################################
line_list = []

with open("工厂_1000.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp[-6:-4])

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
data = pd.DataFrame(line_list,columns=heads)  

number = data.groupby(['LON','LAT']).size().reset_index().sort_values(by=['LON','LAT'],ascending=True)#分组统计
number.rename(columns={0:'工厂_1000'}, inplace=True)#重新命名

df=pd.merge(df,number,how='left',on=['LON','LAT'])
df.describe()

################################长度#########################################
line_list = []
with open("主要道路_1000.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp)

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
data = pd.DataFrame(line_list,columns=heads)  
data.rename(columns={'Shape_Length':'长度'}, inplace=True)#修改列名

data['长度'] = pd.to_numeric(data['长度']) 
data.describe()
    
length = data.groupby(['LON','LAT'])['长度'].sum().reset_index().sort_values(by=['LON','LAT'],ascending=True)#分组统计
length.rename(columns={'长度':'主要道路_1000'}, inplace=True)#重新命名

df=pd.merge(df,length,how='left',on=['LON','LAT'])
df.describe()
################################人口#########################################
line_list = []
with open("人口密度_1000.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp)

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
data = pd.DataFrame(line_list,columns=heads)  
data.rename(columns={'人口密度\r\n':'人口'}, inplace=True)#修改列名

data['人口'] = pd.to_numeric(data['人口']) 
    
density = data.groupby(['LON','LAT'])['人口'].sum().reset_index().sort_values(by=['LON','LAT'],ascending=True)#分组统计
density.rename(columns={'人口':'人口密度_1000'}, inplace=True)#重新命名

df=pd.merge(df,density,how='left',on=['LON','LAT'])
df.describe()
###################################面积########################################
line_list = []
with open("土地利用_3000.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp)

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
data = pd.DataFrame(line_list,columns=heads)  
data.rename(columns={'面积\r\n':'面积','descriptio':'类型'}, inplace=True)#修改列名

data['面积'] = pd.to_numeric(data['面积']) 

area = data.groupby(['LON','LAT','类型'])['面积'].sum().reset_index().sort_values(by=(['LON','LAT','类型']),ascending=True)#分组统计

#test = line_list.groupby(['类型'])['面积'].sum()
Residential = area[area['类型']=='Residential']
Business = area[area['类型']=='Business']
Industrial = area[area['类型']=='Industrial']
Water = area[area['类型']=='Water Features']
Green = area[area['类型']=='Green']

Residential.rename(columns={'面积':'居住_3000'}, inplace=True)#重新命名
Residential = Residential.drop(['类型'],axis=1)
df=pd.merge(df,Residential,how='left',on=['LON','LAT'])

Business.rename(columns={'面积':'商业_3000'}, inplace=True)#重新命名
Business = Business.drop(['类型'],axis=1)
df=pd.merge(df,Business,how='left',on=['LON','LAT'])

Industrial.rename(columns={'面积':'工业_3000'}, inplace=True)#重新命名
Industrial = Industrial.drop(['类型'],axis=1)
df=pd.merge(df,Industrial,how='left',on=['LON','LAT'])

Water.rename(columns={'面积':'水域_3000'}, inplace=True)#重新命名
Water = Water.drop(['类型'],axis=1)
df=pd.merge(df,Water,how='left',on=['LON','LAT'])


Green.rename(columns={'面积':'绿地_3000'}, inplace=True)#重新命名
Green = Green.drop(['类型'],axis=1)
df=pd.merge(df,Green,how='left',on=['LON','LAT'])

df.describe()

##################################污染物#####################################
line_list = []

with open("氮氧化物.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp)

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
data = pd.DataFrame(line_list,columns=heads)  
data.rename(columns={'RASTERVALU\r\n':'氮氧化物'}, inplace=True)#修改列名
#data.rename(columns={'RASTERVALU':'二氧化硫','LAT\r\n':'LAT'}, inplace=True)#修改列名

for j in range(0,data.shape[1]):#将换行符标记为nan
    data.iloc[:,j]=data.iloc[:,j].apply(lambda x: np.nan if x=='\r\n' else x)
#for j in range(0,data.shape[1]):#将换行符标记为nan
#    data.iloc[:,j]=data.iloc[:,j].apply(lambda x: x if x else np.nan)

data['氮氧化物'] = pd.to_numeric(data['氮氧化物']) 
data.fillna(data.mean()['氮氧化物'],inplace=True)#用平均值替代缺失值
data = data[['LON','LAT','氮氧化物']]

df=pd.merge(df,data,how='left',on=['LON','LAT'])
#df.drop(['O3','一氧化氮','一氧化碳','二氧化硫_x','二氧化硫_y'],axis=1,inplace=True) 
##################################气象#####################################
#df.drop(['二氧化硫'],axis=1,inplace=True) 
line_list = []

with open("气温_PM2.5.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp)

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
data = pd.DataFrame(line_list,columns=heads)  
data.rename(columns={'RASTERVALU\r\n':'气温_PM2.5'}, inplace=True)#修改列名

for j in range(0,data.shape[1]):#将换行符标记为nan
    data.iloc[:,j]=data.iloc[:,j].apply(lambda x: np.nan if x=='\r\n' else x)

data['气温_PM2.5'] = pd.to_numeric(data['气温_PM2.5']) 
data['气温_PM2.5']=data['气温_PM2.5'].apply(lambda x: np.nan if x<0 else x)
data.fillna(data.mean()['气温_PM2.5'],inplace=True)#用平均值替代缺失值
data = data[['LON','LAT','气温_PM2.5']]

df=pd.merge(df,data,how='left',on=['LON','LAT'])
df.describe()

#df['风速_NO2']=df['风速_NO2'].apply(lambda x: np.nan if x<0 else x)
#df.fillna(df.mean()['风速_NO2'],inplace=True)#用平均值替代缺失值
##################################二值化变量#####################################
df['1.0']=df['2.0']=df['3.0']=df['4.0']=df['5.0']=df['6.0']=0
df['7.0']=df['8.0']=df['9.0']=df['10.0']=df['12.0']=0
df['11.0']=1

df['工作日']=1

####################################导出######################################
df.to_csv('网格点信息表_temp.csv',index = False,encoding = 'utf_8_sig') 