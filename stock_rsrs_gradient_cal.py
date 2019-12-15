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
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_rsrs_beta_cal'
b1 = 0
df = pd.read_csv(read_dir + os.sep + '000034.SZ.csv', usecols=['ts_code', 'trade_date', 'high', 'low'])
row_num = df.shape[0]
df_rsrs = pd.DataFrame(columns=['ts_code', 'trade_date', 'high', 'low', 'beta'])
for k in range(0, row_num-18):
    i = 0
    j = 0
    x = 0
    y = 0
   # code = df.iloc[k]['ts_code']
    #trade_date = df.iloc[k]['trade_date']
    #price_high = df.iloc[k]['high']
    #price_low = df.iloc[k]['low']
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
    df_rsrs.at[k, 'ts_code'] = df.iloc[i]['ts_code']
    df_rsrs.at[k, 'trade_date'] = df.iloc[i]['trade_date']
    df_rsrs.at[k, 'high'] = df.iloc[i]['high']
    df_rsrs.at[k, 'low'] = df.iloc[i]['low']
    df_rsrs.at[k, 'beta'] = b1
    #print b1,df.iloc[i]['trade_date']
pd.DataFrame.to_csv(df_rsrs, targetdir + os.sep + 'beta_cal.csv', encoding='gbk')

