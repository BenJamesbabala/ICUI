# -*- coding: utf-8 -*-
"""
Created on Tue Jun 11 08:49:11 2019

@author: xin-yi.song
"""

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

###############################导入数据PM2.5#####################################
name_list = []
with open(r'C:\Users\xin-yi.song\Desktop\ICUI\POLLUTION_2\日数据汇总.csv', newline='',encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

result = pd.DataFrame(name_list) 

#result = result.iloc[:,12:result.shape[1]]#删除所有的月份变量
result = result.drop(columns = ['年','月','日','点位名称'])
#result = result.drop(columns = ['O3','一氧化氮','一氧化碳','二氧化硫','氮氧化物','二氧化氮','年','月','日','点位名称'])#有无其他污染物
#result = result.drop(columns = ['二氧化氮','年','月','日','点位名称','工作日'])
col_names = result.columns.values.tolist()

###############################计算相关系数######################################
for element in col_names:
    result[element]=result[element].astype('float64')
result.dtypes

matrix = result.corr('pearson') 
for j in range(0,matrix.shape[1]):#将1标记为空缺值
    matrix.iloc[:,j]=matrix.iloc[:,j].apply(lambda x: np.nan if x==1 else x)

info = matrix.describe()

#################################归一化######################################
#将所有的x,y都进行归一化
#result_scaled = preprocessing.scale(result.values)#标准化
#result_scaled.mean(axis=0)#零均值
#result_scaled.std(axis=0)#标准方差
##print(result_scaled)

min_max_scaler = preprocessing.MinMaxScaler()
result_scaled_minmax = min_max_scaler.fit_transform(result)

data = pd.DataFrame(result_scaled_minmax,columns = col_names)

#################################绘图###########################################

X=data.loc[:,'风速']
Y=data.loc[:,'二氧化氮']
#T=np.arctan2(Y,X)#for color value

#plt.scatter(X,Y,s=75,c=T,alpha=0.5)
plt.scatter(X, Y, s=100, alpha=0.10)

plt.xlabel('water_3000')
plt.ylabel('NO2 concentration')

#plt.xlim((-1.5,1.5))
#plt.ylim((-1.5,1.5))
#plt.xticks(())#隐藏x标签
#plt.yticks(())
plt.show()