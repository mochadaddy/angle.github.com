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
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_ma_20_60_stategy'
target_dir_fill = 'D:/Program Files/tdx/vipdoc/sz/sz_ma_20_60_stategy_fill'
read_dir_annual_return = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare_annual_return/nhsy.csv'
fileNames_week = glob.glob(target_dir + r'\*')
fileNames_week_fill = glob.glob(target_dir_fill + r'\*')

for fileName in fileNames_week:
    try:
        os.remove(fileName)
    except:
        break
for fileName1 in fileNames_week_fill:
    try:
        os.remove(fileName1)
    except:
        break

stock_list = pd.read_csv(read_dir_annual_return, usecols=['ts_code', 'year_annual_return'])
stock_list_20_60 = stock_list[stock_list['year_annual_return'] > 0]
stock_num = stock_list_20_60.shape[0]
for i in range(0, stock_num):
    stock_code = stock_list_20_60.iloc[i]['ts_code']
    df = pd.read_csv(read_dir + os.sep + stock_code + '.csv', usecols=['ts_code', 'trade_date', 'open', 'close',
                                                                       'pct_chg', 'vol', 'amount', 'MA_20'])
    df_aes = df.sort_values('trade_date', ascending=True)
    df_new = df_aes.reset_index(drop=True)
    # 当60天均线高于20天均线时，置flag标志位为1，当60天均线小于20天均线时，置flag标志位为0
    df_new['flag'] = ''
    #df_new['return'] = ''
    mask = df_new['close'] - df_new['MA_20']
    df_new.loc[mask > 0, 'flag'] = 1
    df_new.loc[mask < 0, 'flag'] = 0
    pd.DataFrame.to_csv(df_new, target_dir + os.sep + stock_code + '.csv', encoding='gbk')

read_dir_ma_20_60 = 'D:/Program Files/tdx/vipdoc/sz/sz_ma_20_60_stategy'
read_dir_files = os.listdir(read_dir_ma_20_60)

for stock_file in read_dir_files:
    df1 = pd.read_csv(read_dir_ma_20_60 + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'close', 'open',
                                                                       'pct_chg', 'vol', 'amount', 'MA_20', 'flag'])
    day_trade_num = df1.shape[0]
    df1['money_cal'] = None
    for j in range(0, day_trade_num):
        if df1.iloc[j]['close'] == df1.iloc[j]['MA_20']:
            # 对flag列根据前值填充当前列的空值
            df1['flag'].fillna(method='ffill', inplace=True)
    pd.DataFrame.to_csv(df1, target_dir_fill + os.sep + stock_file, encoding='gbk')





