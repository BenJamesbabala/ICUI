
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 21 00:39:52 2019

@author: xinyisong
"""

import os
import csv
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn import datasets, linear_model


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

columns_1 = ['二氧化硫','氮氧化物','O3','气温','10.0','12.0','风速','LON','工业_1000',
             '9.0','8.0','2.0','7.0','LAT','3.0','1.0','6.0','气压','居住_300',
             '普通道路_100','5.0','加油站_500','商业_100']
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
result_2['工作日']=0

for j in range(0,result_2.shape[1]):#将空标记为nan
    result_2.iloc[:,j]=result_2.iloc[:,j].apply(lambda x: x if x else 0)
    
columns_2 = ['二氧化硫','氮氧化物','O3','气温_PM2.5','10.0','12.0','风速_PM2.5','LON','工业_1000',
             '9.0','8.0','2.0','7.0','LAT','3.0','1.0','6.0','气压_PM2.5','居住_300',
             '普通道路_100','5.0','加油站_500','商业_100']

df2=result_2[columns_2]
df2.rename(columns={'气温_PM2.5':'气温','风速_PM2.5':'风速','气压_PM2.5':'气压'}, inplace=True)#重新命名

################################################################################
#将所有的x,y都进行标准化和归一化
df1_scaled = preprocessing.scale(df1.values)#标准化
df2_scaled = preprocessing.scale(df2.values)

min_max_scaler = preprocessing.MinMaxScaler()
df1_scaled_minmax = min_max_scaler.fit_transform(df1_scaled)
df2_scaled_minmax = min_max_scaler.fit_transform(df2_scaled)

#准备数据
x_train = pd.DataFrame(df1_scaled_minmax, columns = columns_1)
y_train = result_1['PM2.5']

x_predict = pd.DataFrame(df2_scaled_minmax, columns = columns_1)

#随机森林回归
lur = linear_model.LinearRegression()
lur.fit(x_train, y_train)

# 预测 保存预测结果
y_predict = lur.predict(x_predict)
y_predict = pd.Series(y_predict)
 
prediction = pd.concat([df2,y_predict],axis=1)
prediction.rename(columns={0:'PM2.5'}, inplace=True)#重新命名
info = prediction.describe()

##############################################################################
for j in range(0,prediction.shape[1]):
    prediction.iloc[:,j] = pd.to_numeric(prediction.iloc[:,j])

prediction = prediction[['LON','LAT','PM2.5']]
prediction.to_excel('网格点预测值_LUR_PM25.xlsx',index = False,encoding = 'utf_8_sig')
#prediction.to_csv('网格点预测值_LUR_NO2.csv',index = False,encoding = 'utf_8_sig')