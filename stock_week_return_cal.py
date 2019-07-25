# coding: utf-8
import tushare as ts
import pandas as pd
import numpy as np
import os
import glob
import csv
import stock_class as sc

target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_week_return'
read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_week_fill'
fileNames_week = glob.glob(target_dir + r'\*')
for fileName in fileNames_week:
    try:
        os.remove(fileName)
    except:
        break
m = n = 0
read_dir_files = os.listdir(read_dir)
for stock_file in read_dir_files:
    df = pd.read_csv(read_dir + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'close', 'ma5', 'flag'])
    row_num = df.shape[0]
    # print row_num
    buy_price = None
    # 算出股票上市至今的时间长度（以年为单位）
    year_num = round(row_num/52, 2)

    '''
    end_date = '20181228'
    start_date = df.iloc[0]['trade_date']
    start_date_close = df.iloc[0]['close']
    start_date_int = int(start_date)
    start_date_str = str(start_date_int)
    end_date_q4 = end_date[0:4]
    start_date_str_q4 = start_date_str[0:4]
    year_num = int(end_date_q4) - int(start_date_str_q4)
    '''
    k = 0
    for i in range(0, row_num):
        if np.isnan(df.iloc[i]['ma5']):
            continue
        else:
            #if pd.isnull(df.iloc[i - 1]['flag']):
                #df.ix[i, 'money_cal'] = 100
            if df.iloc[i - 1]['flag'] == 0 and df.iloc[i]['flag'] == 1:
                buy_price = df.iloc[i]['close']
                k = k + 1
                if k == 1:
                    df.ix[i, 'money_cal'] = df.ix[i, 'close']
                    buy_price_init = df.ix[i, 'close']
                    max_price = buy_price_init
                    max_withdrawal_rate = 0
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
                    # 取得当前价格之前的最高价格
                    if df.ix[i, 'money_cal'] > max_price:
                        max_price = df.ix[i, 'money_cal']
                    # 计算最大回撤比例
                    withdrawal_rate = 1 - (df.ix[i, 'money_cal'] / max_price)
                    # 比较所有的回撤比例，取得最大的回撤比例
                    if max_withdrawal_rate < withdrawal_rate:
                        max_withdrawal_rate = withdrawal_rate
                    times = round((df.ix[i, 'money_cal']-buy_price_init)/buy_price_init/year_num, 2)
                    times_no_ma5 = round((df.ix[i, 'close']-buy_price_init)/buy_price_init/year_num, 2)
    print (stock_file, times, times_no_ma5, max_withdrawal_rate)
    if times > times_no_ma5:
        m = m + 1
    else:
        n = n + 1
    print (m, n)
    pd.DataFrame.to_csv(df, target_dir + os.sep + stock_file, encoding='gbk')
    
