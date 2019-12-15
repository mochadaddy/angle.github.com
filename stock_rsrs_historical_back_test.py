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


read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_rsrs_beta_cal'
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_rsrs_flag_add'
df = pd.read_csv(read_dir + os.sep + 'beta_cal.csv', usecols=['ts_code', 'trade_date', 'high', 'low', 'close', 'beta'])

row_num = df.shape[0]
df['flag'] = None
for i in range(0, row_num):

    if i > 0:
        if (df.iloc[i]['beta'] >= 1) and (df.iloc[i-1]['beta'] < 1):

            k = i
            while pd.isnull(df.iloc[k]['flag']):
                k = k -1
                if df.iloc[k]['flag'] == 0 or k == 0:
                    df.at[i, 'flag'] = 1
                    break
                elif df.iloc[k]['flag'] == 1:
                    break
        if (df.iloc[i]['beta'] <= 0.8) and (df.iloc[i-1]['beta'] > 0.8):
            j = i
            while pd.isnull(df.iloc[j]['flag']):
                j = j - 1
                if df.iloc[j]['flag'] == 1:
                    df.at[i, 'flag'] = 0
                else:
                   continue
    else:
        continue
pd.DataFrame.to_csv(df, targetdir + os.sep + 'beta_flag.csv', encoding='gbk')




