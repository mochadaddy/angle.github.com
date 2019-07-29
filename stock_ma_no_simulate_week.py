# coding: utf-8
import tushare as ts
import pandas as pd
import os
import csv
import stock_class as sc
import numpy as np

# 联接tushare的api接口
read_dir_week = 'D:/Program Files/tdx/vipdoc/sz/sz_week_return'
szlistfile = os.listdir(read_dir_week)
for stock_file in szlistfile:
    stock_list = pd.read_csv(read_dir_week + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'close', 'ma5',
                                                                           'flag', 'money_cal', 'return_rate'])
    row_num = stock_list.shape[0]
    if (stock_list.iloc[row_num - 1]['flag'] == 1) and (stock_list.iloc[row_num - 2]['flag'] == 0):
        print stock_file
