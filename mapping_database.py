# -*- coding: utf-8 -*-
"""
Created on Sat Jun 15 19:54:56 2019

@author: xinyisong
"""

import os
import csv
import pandas as pd
import numpy as np
from math import sqrt
from sklearn import preprocessing
from sklearn import datasets, linear_model
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

os.getcwd()
os.chdir(r'C:\Users\xin-yi.song\Desktop\ICUI\mapping')


###############################导入数据########################################
name_list = []
with open('日数据汇总.csv', newline='',encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

result = pd.DataFrame(name_list) 
col_names = result.columns.values.tolist()

#result = result.iloc[:,12:result.shape[1]]#删除所有的月份变量
#data = result.drop(columns = ['二氧化氮','年','月','日','点位名称'])#全模型
#data = result.drop(columns = ['O3','一氧化氮','一氧化碳','二氧化硫','氮氧化物','二氧化氮','年','月','日','点位名称'])#有无其他污染物
#data = result.drop(columns = ['二氧化氮','年','月','日','点位名称','工作日'])#有无工作日
#col_names = data.columns.values.tolist()

###################################简单统计####################################
#https://blog.csdn.net/weixin_39791387/article/details/81391621

points_count = result.groupby(['年','月','日'])['点位名称'].size().reset_index().sort_values(by=(['年','月','日']),ascending=True)

result['PM2.5'] = pd.to_numeric(result['PM2.5']) 
result['二氧化氮'] = pd.to_numeric(result['二氧化氮']) 
result.info()
#result.dtypes

average_PM25 = result.groupby(['年','月','日'])['PM2.5'].mean().reset_index().sort_values(by=(['年','月','日']),ascending=True)
#PM2.5最终选择2018年11月11日，站点数量：29，平均PM2.5:55.8132，城市统计：50

average_NO2 = result.groupby(['年','月','日'])['二氧化氮'].mean().reset_index().sort_values(by=(['年','月','日']),ascending=True)
#NO2最终选择2018年11月13日，站点数量：29，平均NO2:47.8342，城市统计：43

###################################挑出那一天的数据#############################

data_PM25 = result[(result['年']=='2018.0') & (result['月']=='11.0') & (result['日']=='11.0')]
data_PM25 = data_PM25[['点位名称','LAT','LON','PM2.5','风速','气温','气压','二氧化硫','一氧化氮','氮氧化物','一氧化碳','O3']]
data_PM25.to_csv('mapping_pollution_PM25.csv',index = False,encoding = 'utf_8_sig')   

data_NO2 = result[(result['年']=='2018.0') & (result['月']=='11.0') & (result['日']=='13.0')]
data_NO2 = data_NO2[['点位名称','LAT','LON','二氧化氮','风速','气温','气压']]
data_NO2.to_csv('mapping_pollution_NO2.csv',index = False,encoding = 'utf_8_sig')  

###################################