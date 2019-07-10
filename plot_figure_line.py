# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 20:48:02 2019

@author: xinyisong
"""

import os
import xlrd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

os.getcwd()
os.chdir(r"C:\Users\xinyisong\Desktop\ICUI\表格分析")
#%matplotlib qt5###，在命令行中输入，用于在窗口显示图片

##############################读取表格##########################################
wb = xlrd.open_workbook("整理_城市数据.xlsx")

sheet = wb.sheet_by_name('Sheet3')

nrows=sheet.nrows #行数
ncols=sheet.ncols #列数
heads = sheet.row_values(0) #从第一行获取列名

df = []

for i in range(1,nrows):
    df.append(sheet.row_values(i)) #汇聚成列表，每个元素是原来sheet表中的一行    
df=pd.DataFrame(df,columns = heads) #可以由列表直接转换为DataFrame，并指定列名

###############################################################################
M = df.loc[0:11,'avg_PM25']
D = df.loc[0:350,'PM2.5']
x = np.linspace(0,350,351)#规定x范围0-350,351个点
#x = list(range(0,351))#0-350,351个点

cond0 =[True if (i<=30) else False for i in x]
cond1 =[True if (i>30 and i<=58) else False for i in x]
cond2 =[True if (i>58 and i<=89) else False for i in x]
cond3 =[True if (i>89 and i<=120) else False for i in x]
cond4 =[True if (i>120 and i<=151) else False for i in x]
cond5 =[True if (i>151 and i<=181) else False for i in x]
cond6 =[True if (i>181 and i<=212) else False for i in x]
cond7 =[True if (i>212 and i<=239) else False for i in x]
cond8 =[True if (i>239 and i<=268) else False for i in x]
cond9 =[True if (i>268 and i<=299) else False for i in x]
cond10 =[True if (i>299 and i<=329) else False for i in x]
cond11 =[True if (i>329 and i<=350) else False for i in x]

def mul(m,c):
    return [i*m for i in c]
    
y = np.sum([mul(M[0],cond0), mul(M[1],cond1), mul(M[2],cond2), mul(M[3],cond3),
            mul(M[4],cond4), mul(M[5],cond5), mul(M[6],cond6), mul(M[7],cond7),
            mul(M[8],cond8), mul(M[9],cond9), mul(M[10],cond10), mul(M[11],cond11),],
            axis=0)

plt.figure(figsize=(15,5))

l1, = plt.plot(x,[25]*351,color='purple',linewidth=2.0,linestyle='-')#The 24h Air Quality Standard of WHO
l2, = plt.plot(x,[35]*351,color='green',linewidth=2.0,linestyle='-')#The 24h Air Quality Standard of China
l3, = plt.plot(x,[75]*351,color='black',linewidth=2.0,linestyle='-')#The Annual Air Quality Standard of China
MM, = plt.plot(x,y,color='red',linewidth=1.5,linestyle='-')
DD, = plt.plot(x,D,color='blue',linewidth=1.5,linestyle='-')

plt.xlim((0,350))
plt.ylim((0,200))
#plt.xlabel('I am x')
plt.ylabel('PM2.5 concentration (μg/m3)')

new_ticks = np.linspace(15,345,12)#print(new_ticks)
plt.xticks(new_ticks,['Jan.','Feb.','Mar.','Apr.','May','Jun.','Jul.','Aug.','Sept.','Oct.','Nov.','Dec.'])#fontproperties='FangSong')
plt.yticks(np.linspace(0,200,11))

plt.text(-8,25,'25',fontdict={'size':8, 'color':'k'})#fontdict={'size':16, 'color':'r'}
plt.text(-8,30,'35',fontdict={'size':8, 'color':'k'})
plt.text(-8,70,'75',fontdict={'size':8, 'color':'k'})

#gca = 'get current axis'
ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data',0))#outward,axes百分比定位
ax.spines['left'].set_position(('data',0))

plt.legend(handles=[l1,l2,l3,MM,DD],labels=['The 24h Air Quality Standard of WHO','The 24h Air Quality Standard of China','The Annual Air Quality Standard of China',
           'Monthly average','Daily average'],loc='best') 
plt.show()