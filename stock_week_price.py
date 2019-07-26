
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

# 联接tushare的api接口
pro = sc.get_tocken()
yesterday = sc.get_sys_date()
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_week'
read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare_annual_return/nhsy.csv'
targetdir_fill = 'D:/Program Files/tdx/vipdoc/sz/sz_week_fill'

fileNames_week = glob.glob(targetdir + r'\*')
fileNames_week_fill = glob.glob(targetdir_fill + r'\*')
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


stock_list = pd.read_csv(read_dir, usecols=['ts_code', 'year_annual_return'])
stock_list_5 = stock_list[stock_list['year_annual_return'] > 0]
#print stock_list_5

stock_num = stock_list_5.shape[0]
for i in range(0, stock_num):
    stock_code = stock_list_5.iloc[i]['ts_code']
    df = ts.pro_bar(ts_code=stock_code, freq='W', adj='hfq', start_date='19910101', end_date=yesterday, ma=[5])
    df_aes = df.sort_values('trade_date', ascending=True)
    df_new = df_aes.reset_index(drop=True)
    # 当周线收盘价高于5周均线时，置flag标志位为1，当周线收盘价低于5周均线时，置flag标志位为0
    df_new['flag'] = ''
    df_new['return'] = ''
    mask = df_new['close'] - df_new['ma5']
    df_new.loc[mask > 0, 'flag'] = 1
    df_new.loc[mask < 0, 'flag'] = 0
    pd.DataFrame.to_csv(df_new, targetdir + os.sep + stock_code + '.csv', encoding='gbk')

read_dir_sz_week = 'D:/Program Files/tdx/vipdoc/sz/sz_week'
read_dir_files = os.listdir(read_dir_sz_week)
for stock_file in read_dir_files:
    df1 = pd.read_csv(read_dir_sz_week + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'close', 'open', 'high',
                                                                       'low', 'pre_close', 'change', 'pct_chg', 'vol',
                                                                       'amount', 'ma5', 'ma_v_5', 'flag'])
    day_trade_num = df1.shape[0]
    for j in range(0, day_trade_num):
        if df1.iloc[j]['close'] == df1.iloc[j]['ma5']:
            # 对flag列根据前值填充当前列的空值
            df1['flag'].fillna(method='ffill', inplace=True)
    pd.DataFrame.to_csv(df1, targetdir_fill + os.sep + stock_file, encoding='gbk')






