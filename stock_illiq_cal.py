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

pro = sc.get_tocken()
read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/combine_cap'
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq'
read_dir_illiq = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq'
target_dir_illiq = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq_compare'
start_date = '20190715'
end_date = '20190816'
# 取年化收益大于0的股票集合
stock_list = sc.get_return_rate(0)
stock_num = stock_list.shape[0]
'''
# 清除文件
fileNames_illiq = glob.glob(target_dir + r'\*')
for fileName in fileNames_illiq:
    try:
        os.remove(fileName)
    except:
        break
'''
for j in range(1341, stock_num):
    stock_code = stock_list.iloc[j]['ts_code']
    df_cap = pd.read_csv(read_dir + os.sep + stock_code + '.csv', usecols=['ts_code', 'trade_date', 'open', 'close',
                                                                           'high', 'low', 'change', 'pct_chg', 'vol',
                                                                           'amount',  'MA_5', 'MA_10',
                                                                           'MA_250', 'circ_mv'])

    df_stock_illiq = pd.DataFrame(columns=['ts_code', 'trade_date', 'illiq', 'illiq' + str(5)])
    row_num = df_cap.shape[0]

    for i in range(0, row_num):

        if str(df_cap.iloc[i]['trade_date']) >= start_date and str(df_cap.iloc[i]['trade_date']) <= end_date:

            #print i
            illiq_neutrilize = np.log10(df_cap.iloc[i]['circ_mv'])
            df_stock_illiq.at[i, 'ts_code'] = df_cap.iloc[i]['ts_code']
            df_stock_illiq.at[i, 'trade_date'] = df_cap.iloc[i]['trade_date']
            illiq = abs(df_cap.iloc[i]['change'] + df_cap.iloc[i]['high'] - df_cap.iloc[i]['low']) * 1.0 / df_cap.iloc[i][
                'amount'] * 10000
            # df.at[i, 'illiq'] = illiq
            df_stock_illiq.at[i, 'illiq_neu'] = illiq_neutrilize
            df_stock_illiq.at[i, 'illiq'] = illiq
            df_stock_illiq.at[i, 'illiq_adjust'] = illiq + illiq_neutrilize
            df_stock_illiq['illiq' + str(5)] = df_stock_illiq['illiq_adjust'].rolling(window=5, center=False).mean()

            df_stock_illiq_new = df_stock_illiq.reset_index(drop=True)
        else:
            continue
        if df_stock_illiq_new.shape[0] != 0:
            pd.DataFrame.to_csv(df_stock_illiq_new, target_dir + os.sep + stock_code + '.csv', encoding='gbk')


df_count = pd.DataFrame()
szlistfile = os.listdir(read_dir_illiq)
for stock_file in szlistfile:
    df_stock_illiq_compare = pd.read_csv(read_dir_illiq + os.sep + stock_file,
                                         usecols=['ts_code', 'trade_date', 'illiq_adjust'])
    #行转列
    df_illiq_transpotion = df_stock_illiq_compare.pivot_table(index='ts_code', columns='trade_date', values='illiq_adjust',
                                                              aggfunc=np.mean)
    df_count = df_count.append(df_illiq_transpotion)
pd.DataFrame.to_csv(df_count, target_dir_illiq + os.sep + 'illiq.csv', encoding='gbk')