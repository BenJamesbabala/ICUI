# -*- coding: utf-8 -*-
"""
Created on Thu Jun 13 23:51:50 2019

@author: xinyisong
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.axisartist as axisartist

#创建画布
#fig = plt.figure(figsize=(10, 5))
#使用axisartist.Subplot方法创建一个绘图区对象ax
#ax = axisartist.Subplot(fig, 111)  
#将绘图区对象添加到画布中
#fig.add_axes(ax)

#通过set_axisline_style方法设置绘图区的底部及左侧坐标轴样式
#"-|>"代表实心箭头："->"代表空心箭头
#ax.axis["bottom"].set_axisline_style("->", size = 1.5)
#ax.axis["left"].set_axisline_style("->", size = 1.5)

#通过set_visible方法设置绘图区的顶部及右侧坐标轴隐藏
#ax.axis["top"].set_visible(False)
#ax.axis["right"].set_visible(False)

x = np.linspace(0,11,12)
y = 0.5*(x-7)**2+5

plt.figure(figsize=(10,5))

plt.plot(x,y,color='k',linewidth=2.0,linestyle='-')

#plt.xlabel('I am x')
plt.ylabel('NO2 concentration (μg/m3)',fontsize=16)
#plt.ylabel('NO2 concentration (μg/m3)')

plt.xticks(x,['Jan.','Feb.','Mar.','Apr.','May','Jun.','Jul.','Aug.','Sept.','Oct.','Nov.','Dec.'],fontsize=16)#fontproperties='FangSong')
plt.yticks(())#隐藏y标签

plt.text(2,20,'The U-shaped change',fontdict={'size':40, 'color':'k'})

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')

plt.show()