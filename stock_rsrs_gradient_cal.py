# coding: utf-8
'''
按照5周均线，填写股票买入卖出标志位
'''
import tushare as ts
import pandas as pd
import os
import glob
import csv
import stock_class as sc
import numpy as np


read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/day_download'
b1 = 0
x = 0
y = 0
df = pd.read_csv(read_dir + os.sep + '002019.SZ.csv', usecols=['ts_code', 'trade_date', 'high', 'low'])
row_num = df.shape[0]
for k in range(0, row_num-18):
    i = 0
    j = 0
    x = 0
    y = 0
    for i in range(0+k, 18+k):
        x = x + df.iloc[i]['low']
        y = y + df.iloc[i]['high']
    x_mean = x / 18
    y_mean = y / 18
    dinominator = 0
    numerator = 0
    for j in range(0+k, 18+k):
        numerator += (df.iloc[j]['low'] - x_mean) * (df.iloc[j]['high'] - y_mean)
        dinominator += (df.iloc[j]['low'] - x_mean) ** 2
    b1 = numerator/dinominator

    print b1,df.iloc[i]['trade_date']









'''
df_gradient = pd.DataFrame()
row_num = df.shape[0]
for i in range(0, row_num):
    if i == 0:
        continue
    else:
        high_devalue = df.iloc[i]['high'] - df.iloc[i-1]['high']
        low_devalue = df.iloc[i]['low'] - df.iloc[i-1]['low']
        if low_devalue == 0:
            continue
        else:
            gradient = high_devalue*1.00/low_devalue
            df_gradient.at[i, 'ts_code'] = df.iloc[i]['ts_code']
            df_gradient.at[i, 'trade_date'] = df.iloc[i]['trade_date']
            df_gradient.at[i, 'gradient'] = gradient
            df_gradient['gradient' + str(5)] = df_gradient['gradient'].rolling(window=18, center=False).mean()
print df_gradient
'''
