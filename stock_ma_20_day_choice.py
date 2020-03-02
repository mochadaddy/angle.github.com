# coding: utf-8
import tushare as ts
import pandas as pd
import os
import csv
import stock_class as sc
import numpy as np

# 联接tushare的api接口
read_dir_week = 'D:/Program Files/tdx/vipdoc/sz/sz_ma_20_60_return'
szlistfile = os.listdir(read_dir_week)
count_rise = 0
count_drop = 0
count_stand_on = 0
count_stand_under = 0
for stock_file in szlistfile:
    stock_list = pd.read_csv(read_dir_week + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'close', 'MA_20',
                                                                           'flag', 'money_cal', 'return_rate'])
    row_num = stock_list.shape[0]
    if (stock_list.iloc[row_num - 1]['flag'] == 1) and (stock_list.iloc[row_num - 2]['flag'] == 0):
        count_rise = count_rise + 1
        print(stock_file[0:9])
    if (stock_list.iloc[row_num - 1]['flag'] == 0) and (stock_list.iloc[row_num - 2]['flag'] == 1):
        count_drop = count_drop + 1
    if stock_list.iloc[row_num - 1]['flag'] == 0:
        count_stand_under = count_stand_under + 1
    if stock_list.iloc[row_num - 1]['flag'] == 1:
        count_stand_on = count_stand_on + 1
#print ()
print(count_rise, count_drop,count_stand_on, count_stand_under)
