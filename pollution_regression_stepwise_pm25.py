# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 22:30:56 2018

@author: songxinyi618
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
os.chdir(r'C:\Users\xinyisong\Desktop\ICUI\POLLUTION_2')


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
data = result.drop(columns = ['二氧化氮','年','月','日','点位名称'])#全模型
#data = result.drop(columns = ['O3','一氧化氮','一氧化碳','二氧化硫','氮氧化物','二氧化氮','年','月','日','点位名称'])#有无其他污染物
#data = result.drop(columns = ['二氧化氮','年','月','日','点位名称','工作日'])#有无工作日

col_names = data.columns.values.tolist()


###############################画散点图########################################

#plt.scatter(data.ix[:,'工业_1000'], data.ix[:,'PM2.5'], s=100, alpha=0.10)
#plt.xlabel('x')
#plt.ylabel('y')
#plt.show()


###############################计算相关系数######################################
for element in col_names:
    data[element]=data[element].astype('float64')
data.dtypes

matrix = data.corr('pearson') 
for j in range(0,matrix.shape[1]):#将1标记为空缺值
    matrix.iloc[:,j]=matrix.iloc[:,j].apply(lambda x: np.nan if x==1 else x)

info = matrix.describe()

##############################挑选相关度超过0.7的################################
#matrix_1 = matrix[matrix>0.7]
rows = matrix.index.values.tolist()
columns = matrix.columns.values.tolist()

factors = []
abandon = []

for i in range(1,matrix.shape[0]):
    for j in range(0,i):
        value = abs(matrix.iloc[i,j])
        pm_i = abs(matrix.ix[i,'PM2.5'])
        pm_j = abs(matrix.ix['PM2.5',j])
        if value>=0.7:
            index = rows[i]
            column = columns[j]
            print('相关度:',value,index,':',pm_i,column,':',pm_j)
            if (pm_i > pm_j):
                factors.append(index)
                abandon.append(column)
                #if column in factors:
                    #factors.remove(column)
            if (pm_i < pm_j) :
                factors.append(column)
                abandon.append(index)
                #if index in factors:
                    #factors.remove(index)

def fun(one_list):
  temp_list=[]
  for one in one_list:
    if one not in temp_list:
      temp_list.append(one)
  return temp_list

#factors = fun(factors)
abandon = fun(abandon)

################################删除同类因素#####################################
data = data.drop(columns=abandon)
heads = data.columns.values.tolist()

abandon_2 = []
for i in range(0,len(heads)):
    for j in range(i+1,len(heads)):
        if heads[i][0:2]==heads[j][0:2]:
            pm_i = abs(matrix.ix[heads[i],'PM2.5'])
            pm_j = abs(matrix.ix['PM2.5',heads[j]])
            if pm_i>pm_j:
                abandon_2.append(heads[j])
            else:
                abandon_2.append(heads[i])
                
abandon_2 = fun(abandon_2)
results = data.drop(columns=abandon_2)

###############################手动挑选#########################################
#cols=['主要道路_500','城区1（外环路）','一氧化碳','离海的距离（米）','工厂_300','水域_500','11.0','公交站_100','绿地_3000']
#result = results.drop(columns=cols)
result = results

################################################################################

#将所有的x,y都进行标准化和归一化
result_scaled = preprocessing.scale(result.values)#标准化
result_scaled.mean(axis=0)#零均值
result_scaled.std(axis=0)#标准方差
#print(result_scaled)
min_max_scaler = preprocessing.MinMaxScaler()
result_scaled_minmax = min_max_scaler.fit_transform(result_scaled)
#print(result_scaled_minmax)

#准备数据
col_names = result.columns.values.tolist()
result_scaled_minmax = pd.DataFrame(result_scaled_minmax, columns = col_names)
x = result_scaled_minmax.drop(columns=['PM2.5'], axis=1)
y = result['PM2.5']

#分割数据
#随机采样20%作为测试，80%作为训练
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=33)

###################################################################################

attributeList = []               # 构造用于存放属性索引的列表
index = range(x_train.shape[1])  # index用于下面代码中的外层for循环
indexSet = set(index)            # 构造由names中的所有属性对应的索引构成的索引集合
#print(index)
oosError_r2 = []                  # 构造用于存放下面代码中的内层for循环每次结束后最小的RMSE
r2_mark = 0

for i in index:
    attSet = set(attributeList)
    attNoSet = indexSet - attSet          # 构造由不在attributeList中的属性索引组成的集合
    attNo = [ii for ii in attNoSet]      # 构造由不在attributeList中的属性索引组成的列表
    attTemp = []
    adj_r2_list = []
    #errorList = []
    #print(attTry)
    #attTry.dtype
    
    for iTry in attNo:
        #print(iTry)
        attTemp = [] + attributeList
        attTemp.append(iTry)
        
        x_train_Temp = x_train.iloc[:,attTemp]
        x_test_Temp = x_test.iloc[:,attTemp]
        
        # 使用scikit包训练线性回归模型
        model = linear_model.LinearRegression()
        model.fit(x_train_Temp, y_train)
        
        #做出预测
        y_predict = model.predict(x_test_Temp)
        
        
        #评价指标
        r2 = r2_score(y_test, y_predict)
        n = x_train_Temp.shape[0]
        p = x_train_Temp.shape[1] #n是样本数量,p是特征数量 
        adj_r2 = 1-((1-r2_score(y_test,y_predict))*(n-1))/(n-p-1)
        rmse = np.sqrt(mean_squared_error(y_test, y_predict)) 
        
        adj_r2_list.append(r2)
        attTemp = []

    r2_max = max(adj_r2_list)               # 选出r2_list中的最大值
    iBest = np.argmax(adj_r2_list)          # 选出r2_list中的最大值对应的新索引
    
    if (r2_max - r2_mark)>0.001:
        attributeList.append(attNo[iBest])   # 利用新索引iBest将attNo中对应的属性索引添加到attributeList中
        oosError_r2.append(r2_max)     # 将errorList中的最小值添加到oosError列表中    
        #oosError.append(errorList[iBest])     # 将errorList中的最小值添加到oosError列表中       
    r2_mark = r2_max
    
#    attributeList.append(attNo[iBest])   # 利用新索引iBest将attNo中对应的属性索引添加到attributeList中
#    oosError_r2.append(r2_max)     # 将errorList中的最小值添加到oosError列表中    
    
names = x_train.columns.values.tolist()
namesList = [names[i] for i in attributeList]
print("\n" + "Best attribute names")
print(namesList)

# 绘制由不同数量的属性构成的线性回归模型在测试集上的RMSE与属性数量的关系图像
#x = range(len(oosError))
#plt.plot(x, oosError, 'k')
#plt.xlabel('Number of Attributes')
#plt.ylabel('Error (RMS)')
#plt.show()

# 绘制红酒口感实际值与预测值之间的散点图
plt.scatter(y_predict, y_test, s=100, alpha=0.10)
plt.xlabel('Predicted value')
plt.ylabel('Actual value')
plt.show()

################################################################################
import statsmodels.api as sm # 最小二乘

#x = sm.add_constant(x.iloc[:,attributeList])
#y = y
x = sm.add_constant(x_train.iloc[:,attributeList]) # 线性回归增加常数项 y=kx+b
y = y_train
regr = sm.OLS(y, x) # 普通最小二乘模型，ordinary least square model
res = regr.fit()    #res.model.endog
# 从模型获得拟合数据
print(res.params)
print(res.summary())

###############################################################################
x_trian_2 = x_train.iloc[:,attributeList]
x_test_2 = x_test.iloc[:,attributeList]

# 使用scikit包训练线性回归模型
model = linear_model.LinearRegression()
model.fit(x_trian_2, y_train)
        
#做出预测
y_predict = model.predict(x_test_2)
                
#评价指标
r2 = r2_score(y_test, y_predict)
n = x_trian_2.shape[0]
p = x_trian_2.shape[1] #n是样本数量,p是特征数量 
adj_r2 = 1-((1-r2_score(y_test,y_predict))*(n-1))/(n-p-1)
rmse = np.sqrt(mean_squared_error(y_test, y_predict)) 

print('r2=',r2)
print('adj_r2=',adj_r2)
print('rmse',rmse)
