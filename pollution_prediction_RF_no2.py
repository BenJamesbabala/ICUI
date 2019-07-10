# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 22:30:56 2018

@author: songxinyi618
"""

import os
import csv
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.ensemble import RandomForestRegressor


os.getcwd()
os.chdir(r"C:\Users\xinyisong\Desktop\ICUI\mapping\mapping_数据库")

###################################导入训练集#################################
name_list = []
with open(r'日数据汇总.csv', newline='',encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

result_1 = pd.DataFrame(name_list) 

columns_1 = ['气温','风速','气压','人口密度_1000','LAT','离海的距离（米）','工作日',
             '主要道路_1000','工业_3000','饭店_1000','水域_3000','普通道路_1000',
             '饭店_3000','LON','绿地_500','主要道路_3000','1.0','3.0','4.0','5.0',
             '6.0','7.0','8.0','9.0','10.0','11.0','12.0']
df1=result_1[columns_1]

##################################导入测试集###################################
name_list = []
with open(r'网格点信息汇总.csv', newline='',encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

result_2 = pd.DataFrame(name_list) 
result_2['工作日']=1

for j in range(0,result_2.shape[1]):#将空标记为nan
    result_2.iloc[:,j]=result_2.iloc[:,j].apply(lambda x: x if x else 0)
    
columns_2 = ['气温_NO2','风速_NO2','气压_NO2','人口密度_1000','LAT','离海的距离（米）','工作日',
             '主要道路_1000','工业_3000','饭店_1000','水域_3000','普通道路_1000',
             '饭店_3000','LON','绿地_500','主要道路_3000','1.0','3.0','4.0','5.0',
             '6.0','7.0','8.0','9.0','10.0','11.0','12.0']

df2=result_2[columns_2]
df2.rename(columns={'气温_NO2':'气温','风速_NO2':'风速','气压_NO2':'气压'}, inplace=True)#重新命名

################################################################################
#将所有的x,y都进行标准化和归一化
df1_scaled = preprocessing.scale(df1.values)#标准化
df2_scaled = preprocessing.scale(df2.values)

min_max_scaler = preprocessing.MinMaxScaler()
df1_scaled_minmax = min_max_scaler.fit_transform(df1_scaled)
df2_scaled_minmax = min_max_scaler.fit_transform(df2_scaled)

#准备数据
x_train = pd.DataFrame(df1_scaled_minmax, columns = columns_1)
y_train = result_1['二氧化氮']

x_predict = pd.DataFrame(df2_scaled_minmax, columns = columns_1)

#随机森林回归
rfr = RandomForestRegressor(n_estimators=400)
rfr.fit(x_train, y_train)

# 预测 保存预测结果
y_predict = rfr.predict(x_predict)
y_predict = pd.Series(y_predict)
 
prediction = pd.concat([df2,y_predict],axis=1)
prediction.rename(columns={0:'NO2'}, inplace=True)#重新命名
info = prediction.describe()

##############################################################################
for j in range(0,prediction.shape[1]):
    prediction.iloc[:,j] = pd.to_numeric(prediction.iloc[:,j])

prediction = prediction[['LON','LAT','NO2']]
#prediction.to_excel('网格点预测值_RF_NO2.xlsx',index = False,encoding = 'utf_8_sig')
prediction.to_csv('网格点预测值_RF_NO2.csv',index = False,encoding = 'utf_8_sig')