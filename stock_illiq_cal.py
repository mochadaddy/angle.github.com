# coding: utf-8
'''
按照日线计算emv指标和maemv指标

'''
import tushare as ts
import pandas as pd
import os
import glob
import csv
import stock_class as sc
import numpy as np


pro = sc.get_tocken()
read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/day_download'
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq'
start_date = '20190101'
end_date = '20190331'
stock_list = sc.get_return_rate(0)
stock_num = stock_list.shape[0]
szlistfile = os.listdir(read_dir)
count = 100
df_stock_illiq = pd.DataFrame(index=range(0, count), columns=['ts_code', 'trade_date', 'illiq', 'illiq' + str(5)])
for j in range(0, stock_num):
    stock_code = stock_list.iloc[j]['ts_code']
    df = pd.read_csv(read_dir + os.sep + stock_code + '.csv', usecols=['ts_code', 'trade_date', 'open', 'close', 'change',
                                                                   'pct_chg', 'vol', 'amount', 'MA_5', 'MA_10', 'MA_250'])
    row_num = df.shape[0]

    for i in range(0, row_num):
        if str(df.iloc[i]['trade_date']) >= start_date and str(df.iloc[i]['trade_date']) <= end_date:
            #print df.ix[i, :]
            df_stock_illiq.at[i, 'ts_code'] = df.iloc[i]['ts_code']
            df_stock_illiq.at[i, 'trade_date'] = df.iloc[i]['trade_date']
            illiq = abs(df.iloc[i]['change'])*1.0/df.iloc[i]['amount']*10000
            df.at[i, 'illiq'] = illiq
            df_stock_illiq.at[i, 'illiq'] = illiq
            df_stock_illiq['illiq'+str(5)] = df['illiq'].rolling(window=5, center=False).mean()

    pd.DataFrame.to_csv(df_stock_illiq, target_dir + os.sep + stock_code + '.csv', encoding='gbk')

