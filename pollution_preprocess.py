# -*- coding: utf-8 -*-
"""
Created on Thu May  9 14:03:06 2019

@author: xin-yi.song
"""

import os
import xlrd
import time 
import numpy as np
import pandas as pd

os.getcwd()
os.chdir(r"C:\Users\Xin-yi.Song\Desktop\ICUI\POLLUTION")

###################################读入污染物大表格#############################
start=time.clock()
wb=xlrd.open_workbook("上海环境监测-非国控站.xlsx")
elapsed=(time.clock()-start)
print("文件读入花费时间:",elapsed)

sheet=wb.sheet_by_name('Sheet1')

nrows=sheet.nrows #行数
ncols=sheet.ncols #列数
heads = sheet.row_values(0) #从第一行获取列名

for i in range(0,len(heads)):#去掉列名中的空格
    heads[i] = heads[i].strip()

rows_list = []

for i in range(1,nrows):
    rows_list.append(sheet.row_values(i)) #汇聚成列表，每个元素是原来sheet表中的一行    
df=pd.DataFrame(rows_list,columns = heads) #可以由列表直接转换为DataFrame，并指定列名 
#print(df[['经度','纬度']])
#df.columns.values.tolist()#获取列名

#df.isna().any()
for j in range(0,df.shape[1]):#将空格标记为nan
    df.iloc[:,j]=df.iloc[:,j].apply(lambda x: np.nan if str(x).isspace() else x)

for j in range(0,df.shape[1]):#将空缺值标记为nan
    df.iloc[:,j]=df.iloc[:,j].apply(lambda x: x if x else np.nan)
    
data = df[['点位名称','年','月','日','时','二氧化氮','PM2.5','风速','气温','气压']]
data = data.dropna()#将所有含有nan项的row删除 
data.isna().any()#已经删除了所有空值 
info = data.describe()#查看数据的描述信息
#info = data.describe().append([data.quantile(0.1),data.quantile(0.2),data.quantile(0.8),data.quantile(0.9)])

#################################设置阈值#######################################
# https://www.aqistudy.cn/historydata/daydata.php?city=%E4%B8%8A%E6%B5%B7
#根据PM2.5历史数据，规定PM2.5的取值范围为5-200 
data = data[(data['PM2.5']>=5) & (data['PM2.5'] <=200)]
data['PM2.5'].describe()

#根据二氧化氮历史数据，规定二氧化氮的取值范围为5-150
data = data[(data['二氧化氮']>=5) & (data['二氧化氮'] <=150)]
data['二氧化氮'].describe()

#查看风速值，规定风速取值范围为0-30
#wind = data['风速'].reset_index().sort_values(by=['风速'],ascending=False).reset_index() #分组统计
#wind.describe()
data = data[data['风速']<=30]
data['风速'].describe()

#查看气温值，规定气温取值范围为超过-5
#temp = data['气温'].reset_index().sort_values(by=['气温'],ascending=True).reset_index() #分组统计
#temp.describe()
data = data[data['气温']>=-5]
data['气温'].describe()

#查看气压值，规定气压取值范围为900-1100
#pre = data['气压'].reset_index().sort_values(by=['气压'],ascending=True).reset_index() #分组统计
#pre.describe()
data = data[(data['气压']>=900) & (data['气压']<=1100)]
data['气压'].describe()

##############################删除少于8小时的数据###############################
number = data.groupby(['点位名称','年','月','日']).size().reset_index().sort_values(by=['点位名称','年','月','日'],ascending=True) #分组统计
number = number[number.loc[:,0]>=8] #将多于8小时的数据保存在number中
number.rename(columns={0:'数量'}, inplace=True)#修改列名

data = pd.merge(data,number,how='left',on=['点位名称','年','月','日'])
data = data.dropna(subset=['数量'])#删除少于8小时的数据

data.reset_index(drop = True,inplace=True)#去掉已经错位的index

#####################################日数据####################################
dd = data.groupby(['点位名称','年','月','日'])['PM2.5','二氧化氮','风速','气温','气压'].mean().reset_index().sort_values(by=['点位名称','年','月','日'],ascending=True)
#test = data[(data['点位名称']=='人民广场') & (data['年']==2016) & (data['月']==7)& (data['日']==31)]

for i in range(0,dd.shape[0]):#去掉点位名称中的空格
    dd.loc[i,'点位名称'] = dd.loc[i,'点位名称'].strip() 

dd.to_csv('日数据.csv',index = True,encoding = 'utf_8_sig')    
 
#####################################月数据####################################
mm = dd.groupby(['点位名称','年','月'])['PM2.5','二氧化氮','风速','气温','气压'].mean().reset_index().sort_values(by=['点位名称','年','月'],ascending=True)
dummies = pd.get_dummies(mm['月'])
mm = mm[['点位名称','年','月','PM2.5','二氧化氮','风速','气温','气压']].join(dummies)

mm.to_csv('月数据.csv',index = True,encoding = 'utf_8_sig')  