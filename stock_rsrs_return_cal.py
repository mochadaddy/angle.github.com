# coding: utf-8
'''
根据标志位得到买入卖出价格，并计算策略收益、资金曲线、最大回撤比例。并与未采用策略的年化收益比较，得出使用
策略的优劣
'''
import pandas as pd
import numpy as np
import os
import glob


read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_rsrs_flag_add'
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_rsrs_return'
df = pd.read_csv(read_dir + os.sep + 'beta_flag.csv',
                 usecols=['ts_code', 'trade_date', 'high', 'low', 'close', 'beta', 'flag'])
row_num = df.shape[0]
buy_price = None
year_num = round(row_num/250, 2)
k = 0
for i in range(0, row_num):
    if np.isnan(df.iloc[i]['flag']):
        continue
    else:
        if df.iloc[i]['flag'] == 1:
            buy_price = df.iloc[i]['close']
            k = k + 1
            if k == 1:
                df.ix[i, 'money_cal'] = df.ix[i, 'close']
                buy_price_init = df.ix[i, 'close']
        if df.iloc[i]['flag'] == 0:
            sell_price = df.iloc[i]['close']
            return_rate = (sell_price - buy_price) / buy_price
            df.ix[i, 'return_rate'] = return_rate
            j = i
            while pd.isnull(df.iloc[j]['money_cal']):
                j = j - 1
            df.ix[i, 'money_cal'] = df.ix[j, 'money_cal'] * return_rate + df.ix[j, 'money_cal']
pd.DataFrame.to_csv(df, target_dir + os.sep + 'rsrs_return.csv', encoding='gbk')

