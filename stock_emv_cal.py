# coding: utf-8
'''
按照日线计算emv指标和maemv指标

'''
import tushare as ts
import pandas as pd
import os
import glob
import csv
import stock_class as sc
import numpy as np


# 联接tushare的api接口
pro = sc.get_tocken()
yesterday = sc.get_sys_date()

read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare'
df = pd.read_csv(read_dir + os.sep + '000001.SZ.csv', usecols=['ts_code', 'trade_date', 'open', 'high', 'low', 'close',
                                                               'pct_chg', 'vol', 'amount', 'MA_5', 'MA_10', 'MA_250'])

row_num = df.shape[0]
for i in range(0, row_num):
    price_high_i = df.ix[i, 'high']
    price_low_i = df.ix[i, 'low']
    vol = df.ix[i, 'vol']
    if i > 0:
        price_high_i_last_day = df.ix[i-1, 'high']
        price_low_i_last_day = df.ix[i-1, 'low']
        em = ((price_high_i + price_low_i)/2 - (price_high_i_last_day - price_low_i_last_day)/2) * (price_high_i -
                                                                                                    price_low_i) / vol
        df.at[i, 'em'] = em
        df['emv'] = df['em'].rolling(window=5, center=False).mean()
        print df.iloc[i]['emv']


