# coding: utf-8
import tushare as ts
import pandas as pd
import numpy as np
import os
import csv
import stock_class as sc

target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_week_return'
read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_week_fill'
read_dir_files = os.listdir(read_dir)
for stock_file in read_dir_files:
    df = pd.read_csv(read_dir + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'close', 'ma5', 'flag'])
    row_num = df.shape[0]
    print row_num
    buy_price = None
    for i in range(0, row_num):
        if np.isnan(df.iloc[i]['ma5']):
            continue
        else:
            if pd.isnull(df.iloc[i - 1]['flag']):
                df.ix[i, 'money_cal'] = 100
            if df.iloc[i - 1]['flag'] == 0 and df.iloc[i]['flag'] == 1:
                buy_price = df.iloc[i]['close']
            if df.iloc[i - 1]['flag'] == 1 and df.iloc[i]['flag'] == 0:
                if buy_price is None:
                    continue
                else:
                    sell_price = df.iloc[i]['close']
                    return_rate = (sell_price - buy_price) / buy_price
                    df.ix[i, 'return_rate'] = return_rate
                    j = i
                    while pd.isnull(df.iloc[j]['money_cal']):
                        j = j - 1
                    df.ix[i, 'money_cal'] = df.ix[j, 'money_cal'] * return_rate + df.ix[j, 'money_cal']

    pd.DataFrame.to_csv(df, target_dir + os.sep + stock_file, encoding='gbk')
