# -*- coding: utf-8 -*-
"""
Created on Tue May  7 19:47:03 2019

@author: xin-yi.song
"""

import os
import xlrd
import pandas as pd

os.getcwd()
os.chdir(r"C:\Users\Xin-yi.Song\Desktop\ICUI\POINTS\数据库")

################################读取大表格#####################################
wb=xlrd.open_workbook("监测点信息汇总.xlsx")

sheet=wb.sheet_by_name('Sheet1')

nrows=sheet.nrows #行数
ncols=sheet.ncols #列数
heads = sheet.row_values(0) #从第一行获取列名

df = []

for i in range(1,nrows):
    df.append(sheet.row_values(i)) #汇聚成列表，每个元素是原来sheet表中的一行    
df=pd.DataFrame(df,columns = heads) #可以由列表直接转换为DataFrame，并指定列名
df.rename(columns={' 点位名称 ':'点位名称'}, inplace=True) #重新命名

for i,element in enumerate(df['点位名称']):#删除点位名称中的空格
    df.loc[i,'点位名称'] = df.loc[i,'点位名称'].strip() 
            
################################个数#######################################
line_list = []

with open("公交站_100.txt", newline='',encoding='utf-8') as f:
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

mm = pd.DataFrame(number)
mm.rename(columns={0:'公交站_100'}, inplace=True)#重新命名

for i,element in enumerate(mm['点位名称']):#删除点位名称中的空格
    mm.loc[i,'点位名称'] = mm.loc[i,'点位名称'].strip() 

data=pd.merge(data,mm,how='left',on=['点位名称'])

################################长度+人口#########################################
line_list = []

with open("人口密度_100.txt", newline='',encoding='utf-8') as f:
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
line_list.rename(columns={2:'点位名称',34:'人口'}, inplace=True)#修改列名

for i,element in enumerate(line_list['人口']):#将长度改为浮点数
    line_list.loc[i,'人口'] = float(line_list.loc[i,'人口'])
    
number = line_list.groupby(['点位名称'])['人口'].sum().reset_index().sort_values(by=['点位名称'],ascending=True)#分组统计

nn = pd.DataFrame(number)
nn.rename(columns={'人口':'人口密度_100'}, inplace=True)#重新命名

for i,element in enumerate(nn['点位名称']):#删除点位名称中的空格
    nn.loc[i,'点位名称'] = nn.loc[i,'点位名称'].strip() 

data=pd.merge(data,nn,how='left',on=['点位名称'])

###################################面积########################################
line_list = []

with open("土地利用_100.txt", newline='',encoding='utf-8') as f:
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
line_list.rename(columns={2:'点位名称',13:'类型',16:'面积'}, inplace=True)#修改列名

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

Residential.rename(columns={'面积':'居住_100'}, inplace=True)#重新命名
Residential = Residential.drop(['类型'],axis=1)
data=pd.merge(data,Residential,how='left',on=['点位名称'])

Business.rename(columns={'面积':'商业_100'}, inplace=True)#重新命名
Business = Business.drop(['类型'],axis=1)
data=pd.merge(data,Business,how='left',on=['点位名称'])

Industrial.rename(columns={'面积':'工业_100'}, inplace=True)#重新命名
Industrial = Industrial.drop(['类型'],axis=1)
data=pd.merge(data,Industrial,how='left',on=['点位名称'])

Water.rename(columns={'面积':'水域_100'}, inplace=True)#重新命名
Water = Water.drop(['类型'],axis=1)
data=pd.merge(data,Water,how='left',on=['点位名称'])


Green.rename(columns={'面积':'绿地_100'}, inplace=True)#重新命名
Green = Green.drop(['类型'],axis=1)
data=pd.merge(data,Green,how='left',on=['点位名称'])

####################################导出######################################
data.to_csv('监测点信息汇总_100.csv',index = False,encoding = 'utf_8_sig') 