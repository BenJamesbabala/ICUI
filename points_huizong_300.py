# -*- coding: utf-8 -*-
"""
Created on Tue May  7 19:47:03 2019

@author: xin-yi.song
"""

import os
import csv
import pandas as pd

os.getcwd()
os.chdir(r"C:\Users\Xin-yi.Song\Desktop\ICUI\POINTS_2\数据库-新")

################################读取大表格#####################################
name_list = []

with open('监测点信息汇总_新_100.csv', newline='',encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

name_list = pd.DataFrame(name_list) 
#name_list.columns.values.tolist()#获取列名
#name_list.isna()#判断空值

for j in range(0,name_list.shape[1]):#将空缺值标记为0
    name_list.iloc[:,j]=name_list.iloc[:,j].apply(lambda x: x if x else 0)
    
data = name_list
          
################################个数#######################################
line_list = []
with open("加油站_300.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp)

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
line_list = pd.DataFrame(line_list)  

#data = line_list[[2,14,10,11]]
#data.rename(columns={2:'点位名称', 14:'name', 10:'area', 11:'city'}, inplace=True)
line_list.rename(columns={2:'点位名称'}, inplace=True)#修改列名
number = line_list.groupby(['点位名称']).size().reset_index().sort_values(by=['点位名称'],ascending=True)#分组统计

number.rename(columns={0:'加油站_300'}, inplace=True)#重新命名

for i,element in enumerate(number['点位名称']):#删除点位名称中的空格
    number.loc[i,'点位名称'] = number.loc[i,'点位名称'].strip() 

data=pd.merge(data,number,how='left',on=['点位名称'])

################################长度#########################################
line_list = []
with open("普通道路_300.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp)

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
line_list = pd.DataFrame(line_list)  

#data = line_list[[2,14,10,11]]
#data.rename(columns={2:'点位名称', 14:'name', 10:'area', 11:'city'}, inplace=True)
line_list.rename(columns={6:'点位名称',10:'普通道路_300'}, inplace=True)#修改列名

for i,element in enumerate(line_list['普通道路_300']):#将长度改为浮点数
    line_list.loc[i,'普通道路_300'] = float(line_list.loc[i,'普通道路_300'])
    
number = line_list.groupby(['点位名称'])['普通道路_300'].sum().reset_index().sort_values(by=['点位名称'],ascending=True)#分组统计

for i,element in enumerate(number['点位名称']):#删除点位名称中的空格
    number.loc[i,'点位名称'] = number.loc[i,'点位名称'].strip() 

data=pd.merge(data,number,how='left',on=['点位名称'])
#data.columns.values.tolist()#获取列名
#data.drop(['人口密度_300'],axis=1,inplace=True)

################################人口#########################################
line_list = []
with open("人口密度_300.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp)

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
line_list = pd.DataFrame(line_list)  

#data = line_list[[2,14,10,11]]
#data.rename(columns={2:'点位名称', 14:'name', 10:'area', 11:'city'}, inplace=True)
line_list.rename(columns={2:'点位名称',33:'人口密度_300'}, inplace=True)#修改列名

for i,element in enumerate(line_list['人口密度_300']):#将长度改为浮点数
    line_list.loc[i,'人口密度_300'] = float(line_list.loc[i,'人口密度_300'])
    
number = line_list.groupby(['点位名称'])['人口密度_300'].sum().reset_index().sort_values(by=['点位名称'],ascending=True)#分组统计

for i,element in enumerate(number['点位名称']):#删除点位名称中的空格
    number.loc[i,'点位名称'] = number.loc[i,'点位名称'].strip() 

data=pd.merge(data,number,how='left',on=['点位名称'])
#data.columns.values.tolist()#获取列名
#data.drop(['人口密度_300'],axis=1,inplace=True)

###################################面积########################################
line_list = []
with open("土地利用_300.txt", newline='',encoding='utf-8') as f:
    lines = f.readlines()
       
    for line in lines:
        #print(line,)
        line_temp = line.split(',')
        line_list.append(line_temp)

heads = line_list[0]#记录表头
del(line_list[0])#删除表头
line_list = pd.DataFrame(line_list)  

#data = line_list[[2,14,10,11]]
#data.rename(columns={2:'点位名称', 14:'name', 10:'area', 11:'city'}, inplace=True)
line_list.rename(columns={2:'点位名称',12:'类型',14:'面积'}, inplace=True)#修改列名

for i,element in enumerate(line_list['面积']):#将面积改为浮点数
    line_list.loc[i,'面积'] = float(line_list.loc[i,'面积'])
    
number = line_list.groupby(['点位名称','类型'])['面积'].sum().reset_index().sort_values(by=(['点位名称','类型']),ascending=True)#分组统计

for i,element in enumerate(number['点位名称']):#删除点位名称中的空格
    number.loc[i,'点位名称'] = number.loc[i,'点位名称'].strip() 

#test = line_list.groupby(['类型'])['面积'].sum()
Residential = number[number['类型']=='Residential']
Business = number[number['类型']=='Business']
Industrial = number[number['类型']=='Industrial']
Water = number[number['类型']=='Water Features']
Green = number[number['类型']=='Green']

Residential.rename(columns={'面积':'居住_300'}, inplace=True)#重新命名
Residential = Residential.drop(['类型'],axis=1)
data=pd.merge(data,Residential,how='left',on=['点位名称'])

Business.rename(columns={'面积':'商业_300'}, inplace=True)#重新命名
Business = Business.drop(['类型'],axis=1)
data=pd.merge(data,Business,how='left',on=['点位名称'])

Industrial.rename(columns={'面积':'工业_300'}, inplace=True)#重新命名
Industrial = Industrial.drop(['类型'],axis=1)
data=pd.merge(data,Industrial,how='left',on=['点位名称'])

Water.rename(columns={'面积':'水域_300'}, inplace=True)#重新命名
Water = Water.drop(['类型'],axis=1)
data=pd.merge(data,Water,how='left',on=['点位名称'])


Green.rename(columns={'面积':'绿地_300'}, inplace=True)#重新命名
Green = Green.drop(['类型'],axis=1)
data=pd.merge(data,Green,how='left',on=['点位名称'])

####################################导出######################################
data.to_csv('监测点信息汇总_新_300.csv',index = False,encoding = 'utf_8_sig') 