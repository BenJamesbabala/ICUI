# -*- coding: utf-8 -*-
"""
Created on Tue Dec 25 22:30:56 2018

@author: songxinyi618
"""

import csv
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error

################################################################################
name_list = []
with open(r'C:\Users\xinyisong\Desktop\ICUI\POLLUTION_2\月数据汇总.csv', newline='',encoding='UTF-8-sig') as f:
    reader = csv.DictReader(f)
    for row in reader:
        #print(row)
        row = dict(row)
        name_list.append(row)

result = pd.DataFrame(name_list) 

#result = result.iloc[:,12:result.shape[1]]#删除所有的月份变量
result = result.drop(columns = ['二氧化氮','年','月','点位名称'])
col_names = result.columns.values.tolist()

################################################################################
#将所有的x,y都进行标准化和归一化
result_scaled = preprocessing.scale(result.values)#标准化
#result_scaled.mean(axis=0)#零均值
#result_scaled.std(axis=0)#标准方差
#print(result_scaled)
min_max_scaler = preprocessing.MinMaxScaler()
result_scaled_minmax = min_max_scaler.fit_transform(result_scaled)
#print(result_scaled_minmax)

#准备数据
result2 = pd.DataFrame(result_scaled_minmax, columns = col_names)
x = result2.drop(columns=['PM2.5'], axis=1)
y = result['PM2.5']

#分割数据
#随机采样20%作为测试，80%作为训练
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=33)

#随机森林回归
rfr = RandomForestRegressor(n_estimators=400)
rfr.fit(x_train, y_train)

# 预测 保存预测结果
y_predict_1 = rfr.predict(x_test)
scores_1 = cross_val_score(rfr, x_test, y_test)
print('score:',scores_1.mean()) 
 
r2_1 = r2_score(y_test, y_predict_1)
print('R2:',r2_1)

rmse_1 = np.sqrt(mean_squared_error(y_test, y_predict_1))
print('RMSE', rmse_1)


#RF特征重要性选择
imp = rfr.feature_importances_
imp = pd.DataFrame({'feature': x_train.columns, '重要度': imp})
#imp[['feature','score']].plot(kind='bar', stacked=True)  
imp = imp.sort_values(['重要度'], ascending=[0]).reset_index()#按照特征重要性, 进行降序排列, 最重要的特征在最前面
print(imp)

###############################进行特征筛选#####################################
#筛选前30个特征 
select_feature=imp['feature'][:30]
x_train_feature=x_train.loc[:,select_feature]
x_test_feature=x_test.loc[:,select_feature]

#调整后预测
rfr2 = RandomForestRegressor(n_estimators=400)
rfr2.fit(x_train_feature,y_train)

# 预测 保存预测结果
y_predict_2 = rfr2.predict(x_test_feature)
scores_2 = cross_val_score(rfr2, x_test_feature, y_test)
print('score:',scores_2.mean())  

r2_2 = r2_score(y_test, y_predict_2)
print('R2:',r2_2)

n = x_train_feature.shape[0] #n是样本数量
p = x_train_feature.shape[1] #p是特征数量
r2_adj_2=1-((1-r2_score(y_test,y_predict_2))*(n-1))/(n-p-1)
print('R2_adj:',r2_adj_2)

rmse_2 = np.sqrt(mean_squared_error(y_test, y_predict_2)) 
print('RMSE:',rmse_2)

##############################################################################
import matplotlib.pyplot as plt
plt.scatter(y_predict_2, y_test, s=100, alpha=0.10)
plt.xlabel('Predicted value')
plt.ylabel('Actual value')
plt.show()