# -*- coding: utf-8 -*-
"""
Created on Thu May  2 18:16:46 2019

@author: xin-yi.song
"""

import os
import xlrd
import time
import pandas as pd

os.getcwd()
os.chdir("C:/Users/xinyisong/Desktop/ICUI/area")

start=time.clock()

wb=xlrd.open_workbook("上海环境监测-非国控站.xlsx")
#wb.get_sheet_names()

elapsed=(time.clock()-start)
print("文件读入花费时间:",elapsed)

sheet=wb.sheet_by_name('Sheet1')

nrows=sheet.nrows #行数
ncols=sheet.ncols #列数
heads = sheet.row_values(0) #从第一行获取列名

sheet.row_types(2) #参数2代表第2行
#0      XL_CELL_EMPTY      empty string
#1      XL_CELL_TEXT       a Unicode string
#2      XL_CELL_NUMBER     float
#3      XL_CELL_DATE       float
#4      XL_CELL_BOOLEAN    int; 1 means TRUE, 0 means FALSE
#5      XL_CELL_ERROR      int representing internal Excel codes; for a text representation, refer to the supplied dictionary error_text_from_code
#6      XL_CELL_BLANK      empty string ''. Note: this type will appear only when open_workbook(..., formatting_info=True) is used.

rows_list = []

for i in range(1,nrows):
    rows_list.append(sheet.row_values(i)) #汇聚成列表，每个元素是原来sheet表中的一行    
df=pd.DataFrame(rows_list,columns = heads) #可以由列表直接转换为DataFrame，并指定列名 

points=df[[' 点位名称 ',' 经度 ',' 纬度 ']] #按列名选择多列必须加双括号
points=points.drop_duplicates([' 点位名称 ',' 经度 ',' 纬度 '], keep='first')
print(points)
points.to_csv(r'C:\Users\xinyisong\Desktop\ICUI\area\监测点经纬度.csv',index = False,encoding = 'utf_8_sig')  