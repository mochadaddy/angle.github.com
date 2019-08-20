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
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/combine_cap'
start_date = '20190716'
end_date = '20190816'

'''
# 清除文件
fileNames_illiq = glob.glob(target_dir + r'\*')
for fileName in fileNames_illiq:
    try:
        os.remove(fileName)
    except:
        break
'''

df_cap = pd.DataFrame(columns=['ts_code', 'trade_date', 'open', 'close', 'high', 'low', 'change', 'pct_chg', 'vol',
                               'amount', 'MA_5', 'MA_10', 'MA_250', 'circ_mv'])
szlistfile = os.listdir(read_dir)
for stock_file in szlistfile:
    stock_code = stock_file[:9]
    df = pd.read_csv(read_dir + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'open', 'close', 'high', 'low',
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
        pd.DataFrame.to_csv(df, target_dir + os.sep + stock_file, encoding='gbk')
    else:
        continue
