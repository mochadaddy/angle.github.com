# coding: utf-8
'''
按照日线计算emv指标和maemv指标
'''
import tushare as ts
import pandas as pd
import os
import time
from datetime import datetime as dt
import datetime as d
import glob
import csv
import stock_class as sc
import numpy as np

read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/day_download'
read_dir_annual_return = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare_annual_return/nhsy.csv'
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/combine_cap'
start_date = '20190723'
end_date = '20190823'


# 清除文件
fileNames_illiq = glob.glob(target_dir + r'\*')
for fileName in fileNames_illiq:
    try:
        os.remove(fileName)
    except:
        break

stock_list = pd.read_csv(read_dir_annual_return, usecols=['ts_code', 'year_annual_return'])
stock_list_0 = stock_list[stock_list['year_annual_return'] > 0]
stock_num = stock_list_0.shape[0]

df_cap = pd.DataFrame(columns=['ts_code', 'trade_date', 'open', 'close', 'high', 'low', 'change', 'pct_chg', 'vol',
                               'amount', 'MA_5', 'MA_10', 'MA_250', 'circ_mv'])
#szlistfile = os.listdir(read_dir)
for j in range(0, stock_num):
    stock_code = stock_list_0.iloc[j]['ts_code']
    #stock_code = stock_file[:9]
    df = pd.read_csv(read_dir + os.sep + stock_code + '.csv', usecols=['ts_code', 'trade_date', 'open', 'close', 'high', 'low',
                                                              'change', 'pct_chg', 'vol', 'amount', 'MA_5', 'MA_10',
                                                              'MA_250'])
    row_num = df.shape[0]
    for i in range(0, row_num):
        date = str(df.iloc[i]['trade_date'])
        if date >= start_date and date<=end_date:
            df_cap = sc.get_stock_cap(stock_code, date)
            if df_cap is None:
                continue
            else:
                df.at[i, 'circ_mv'] = df_cap.iloc[0]['circ_mv']
        else:
            continue
    if 'circ_mv' in df:
        pd.DataFrame.to_csv(df, target_dir + os.sep + stock_code + '.csv', encoding='gbk')
    else:
        continue
