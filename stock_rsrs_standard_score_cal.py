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

read_dir_annual_return = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare_annual_return/nhsy.csv'
read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_rsrs_week_beta_cal'
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_rsrs_standard_score_cal_week'

fileNames_week = glob.glob(target_dir + r'\*')
for fileName in fileNames_week:
    try:
        os.remove(fileName)
    except:
        break

read_dir_files = os.listdir(read_dir)
stock_list = pd.read_csv(read_dir_annual_return, usecols=['ts_code', 'year_annual_return'])
stock_list_5 = stock_list[stock_list['year_annual_return'] > 0]
stock_num = stock_list_5.shape[0]
M = 122

#for stock_file in read_dir_files:
for p in range(0, stock_num):
    stock_code = stock_list_5.iloc[p]['ts_code']
    #df = pd.read_csv(read_dir + os.sep + stock_code + '.csv', usecols=['ts_code', 'trade_date', 'high', 'low', 'close', 'beta'])
    df_standard_score_cal = pd.DataFrame()
#    row_num = df.shape[0]
#    df['flag'] = None
    df = pd.read_csv(read_dir + os.sep + stock_code + '.csv', usecols=['ts_code', 'trade_date', 'high', 'low', 'close', 'beta'])
    row_num = df.shape[0]
    #M = 600
    for i in range(0, row_num):

        if i >= M:
            df_standard_score_cal.at[i, 'ts_code'] = df.iloc[i]['ts_code']
            df_standard_score_cal.at[i, 'trade_date'] = df.iloc[i]['trade_date']
            df_standard_score_cal.at[i, 'high'] = df.iloc[i]['high']
            df_standard_score_cal.at[i, 'low'] = df.iloc[i]['low']
            df_standard_score_cal.at[i, 'close'] = df.iloc[i]['close']
            df_standard_score_cal.at[i, 'beta'] = df.iloc[i]['beta']
            average = df['beta'].rolling(window=M, center=False).mean()
            standard_score = df['beta'].rolling(window=M, center=False).std()
            #print df.iloc[i]['beta']
            #print average[i]
            #print standard_score[i]
            temp = (df.iloc[i]['beta'] - average[i]) / standard_score[i]
            df_standard_score_cal.at[i, 'standard_score'] = temp

            #print df.iloc[i]['standard_score']
            #df_standard_score_cal.at[i,'standard_score'] = df.iloc[i]['standard_score']
        else:
            continue
    df_standard_score_cal_new = df_standard_score_cal.reset_index(drop=True)
    row_num_rsrs = df_standard_score_cal_new.shape[0]
    if row_num_rsrs == 0:
        continue
    else:
        pd.DataFrame.to_csv(df_standard_score_cal_new, target_dir + os.sep + stock_code + '.csv', encoding='gbk')
'''
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
            while pd.isnull(df.iloc[j]['flag']) and j >= 0:
                j = j - 1
                if df.iloc[j]['flag'] == 1:
                    df.at[i, 'flag'] = 0
                else:
                   continue
    else:
        continue
pd.DataFrame.to_csv(df, targetdir + os.sep + stock_code + '.csv', encoding='gbk')
'''




