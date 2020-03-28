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


read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_rsrs_standard_score_cal_week'
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_rsrs_flag_add_week'


fileNames_week = glob.glob(targetdir + r'\*')
for fileName in fileNames_week:
    try:
        os.remove(fileName)
    except:
        break

#read_dir_files = os.listdir(read_dir)
#stock_list = pd.read_csv(read_dir_annual_return, usecols=['ts_code', 'year_annual_return'])
#stock_list_5 = stock_list[stock_list['year_annual_return'] > 0]
#stock_num = stock_list_5.shape[0]
#for stock_file in read_dir_files:
read_dir_files = os.listdir(read_dir)
for stock_rsrs_file in read_dir_files:
    df_rsrs = pd.read_csv(read_dir + os.sep + stock_rsrs_file, usecols=['ts_code', 'trade_date', 'high', 'low', 'close', 'beta', 'standard_score'])
    df_rsrs['flag'] = None
    row_num = df_rsrs.shape[0]

    for i in range(0, row_num):
        if df_rsrs.iloc[i]['standard_score'] > 0.7:
            k = i
            while df_rsrs.iloc[k]['flag'] is None:
                k = k - 1
                if df_rsrs.iloc[k]['flag'] == 0 or k == -1:
                    df_rsrs.at[i, 'flag'] = 1
                    break
                elif df_rsrs.iloc[k]['flag'] == 1:
                    break
        if df_rsrs.iloc[i]['standard_score'] < -0.7:
            j = i
            while (df_rsrs.iloc[j]['flag'] is None) and j > 0:
                j = j - 1
                if df_rsrs.iloc[j]['flag'] == 1:
                    df_rsrs.at[i, 'flag'] = 0
                    break
                elif df_rsrs.iloc[j]['flag'] == 0:
                    break
    pd.DataFrame.to_csv(df_rsrs, targetdir + os.sep + stock_rsrs_file, encoding='gbk')




