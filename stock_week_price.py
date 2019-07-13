# coding: utf-8
import tushare as ts
import pandas as pd
import os
import csv
import stock_class as sc
import numpy as np


# 联接tushare的api接口
pro = sc.get_tocken()
yestorday = sc.get_sys_date()
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_week'
read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_nhsy/nhsy.csv'

stock_list = pd.read_csv(read_dir, usecols=['ts_code', 'year_annual_return'])
stock_list_5 = stock_list[stock_list['year_annual_return'] >= 10]
#print stock_list_5

stock_num = stock_list_5.shape[0]
for i in range(0, stock_num):
    stock_code = stock_list.iloc[i]['ts_code']
    df = ts.pro_bar(ts_code=stock_code, freq='W', adj='hfq', start_date='19910101', end_date=yestorday, ma=[5])
    df_aes = df.sort_values('trade_date', ascending=True)
    df_new = df_aes.reset_index(drop=True)
    # 当周线收盘价高于5周均线时，置flag标志位为1，当周线收盘价低于5周均线时，置flag标志位为0
    df_new['flag'] = ''
    df_new['return'] = ''
    mask = df_new['close'] - df_new['ma5']
    df_new.loc[mask > 0, 'flag'] = 1
    df_new.loc[mask < 0, 'flag'] = 0
    pd.DataFrame.to_csv(df_new, targetdir + os.sep + stock_code + '.csv', encoding='gbk')


