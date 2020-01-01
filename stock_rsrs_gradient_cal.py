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
read_dir_rsrs = 'D:/Program Files/tdx/vipdoc/sz/sz_rsrs_beta_cal'
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_rsrs_beta_cal'
parameter_day_period = 18
b1 = 0
read_dir_files = os.listdir(read_dir)
read_dir_files_rsrs = os.listdir(read_dir_rsrs)
for stock_file_download in read_dir_files:
    for stock_file_rsrs in read_dir_files_rsrs:
        if stock_file_download == stock_file_rsrs:
            df_download = pd.read_csv(read_dir + os.sep + stock_file_download,
                             usecols=['ts_code', 'trade_date', 'high', 'low', 'close'])
            df_rsrs = pd.read_csv(read_dir_rsrs + os.sep + stock_file_rsrs,
                             usecols=['ts_code', 'trade_date', 'high', 'low', 'close'])
            row_num = df_download.shape[0]
            row_num_rsrs = df_rsrs.shape[0]
            download_date = df_download.iloc[row_num-1]['trade_date']
            rsrs_date = df_rsrs.iloc[row_num_rsrs-1]['trade_date']
            if rsrs_date < download_date:
                d_value = row_num - row_num_rsrs - parameter_day_period
                while d_value > 0:
                    i = 0
                    j = 0
                    x = 0
                    y = 0
                    for i in range(row_num_rsrs, row_num_rsrs+parameter_day_period):
                        x = x + df_download.iloc[i]['low']
                        y = y + df_download.iloc[i]['high']
                    x_mean = x / parameter_day_period
                    y_mean = y / parameter_day_period
                    dinominator = 0
                    numerator = 0
                    for j in range(row_num_rsrs, row_num_rsrs+parameter_day_period):
                        numerator += (df_download.iloc[j]['low'] - x_mean) * (df_download.iloc[j]['high'] - y_mean)
                        dinominator += (df_download.iloc[j]['low'] - x_mean) ** 2
                    b1 = numerator / dinominator
                    df_rsrs.at[j, 'ts_code'] = df_download.iloc[j]['ts_code']
                     #df_download.iloc[row_num_rsrs+parameter_day_period-1]['trade_date']
                    d_value = d_value - 1







            #print 'yes'
            break
        else:
            continue


            #df = pd.read_csv(read_dir + os.sep + '000034.SZ.csv', usecols=['ts_code', 'trade_date', 'high', 'low', 'close'])
            #df_rsrs_read = pd.read_csv(read_dir + os.sep + '000034.SZ.csv', usecols=['ts_code', 'trade_date', 'high', 'low', 'close'])
            #row_num = df.shape[0]

'''
df_rsrs = pd.DataFrame(columns=['ts_code', 'trade_date', 'high', 'low', 'close', 'beta'])
for k in range(0, row_num-parameter_day_period):
    i = 0
    j = 0
    x = 0
    y = 0
   # code = df.iloc[k]['ts_code']
    #trade_date = df.iloc[k]['trade_date']
    #price_high = df.iloc[k]['high']
    #price_low = df.iloc[k]['low']
    for i in range(0+k, parameter_day_period+k):
        x = x + df.iloc[i]['low']
        y = y + df.iloc[i]['high']
    x_mean = x / parameter_day_period
    y_mean = y / parameter_day_period
    dinominator = 0
    numerator = 0
    for j in range(0+k, parameter_day_period+k):
        numerator += (df.iloc[j]['low'] - x_mean) * (df.iloc[j]['high'] - y_mean)
        dinominator += (df.iloc[j]['low'] - x_mean) ** 2
    b1 = numerator/dinominator
    df_rsrs.at[k, 'ts_code'] = df.iloc[i]['ts_code']
    df_rsrs.at[k, 'trade_date'] = df.iloc[i]['trade_date']
    df_rsrs.at[k, 'high'] = df.iloc[i]['high']
    df_rsrs.at[k, 'low'] = df.iloc[i]['low']
    df_rsrs.at[k, 'close'] = df.iloc[i]['close']
    df_rsrs.at[k, 'beta'] = b1
    #print b1,df.iloc[i]['trade_date']
pd.DataFrame.to_csv(df_rsrs, targetdir + os.sep + '000034.SZ.csv', encoding='gbk')
'''












