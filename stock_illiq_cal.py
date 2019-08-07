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
read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/day_download'
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq'
read_dir_illiq = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq'
target_dir_illiq = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq_compare'
start_date = '20190301'
end_date = '20190630'
stock_list = sc.get_return_rate(0)
stock_num = stock_list.shape[0]

'''
fileNames_week = glob.glob(target_dir + r'\*')
for fileName in fileNames_week:
    try:
        os.remove(fileName)
    except:
        break
for j in range(0, stock_num):
    stock_code = stock_list.iloc[j]['ts_code']
    df = pd.read_csv(read_dir + os.sep + stock_code + '.csv', usecols=['ts_code', 'trade_date', 'open', 'close', 'change',
                                                                   'pct_chg', 'vol', 'amount', 'MA_5', 'MA_10', 'MA_250'])
    row_num = df.shape[0]
    #count = 100
    df_stock_illiq = pd.DataFrame(columns=['ts_code', 'trade_date', 'illiq', 'illiq' + str(5)])
    for i in range(0, row_num):
        if str(df.iloc[i]['trade_date']) >= start_date and str(df.iloc[i]['trade_date']) <= end_date:
            #print df.ix[i, :]
            df_stock_illiq.at[i, 'ts_code'] = df.iloc[i]['ts_code']
            df_stock_illiq.at[i, 'trade_date'] = df.iloc[i]['trade_date']
            illiq = abs(df.iloc[i]['change'])*1.0/df.iloc[i]['amount']*10000
            df.at[i, 'illiq'] = illiq
            df_stock_illiq.at[i, 'illiq'] = illiq
            df_stock_illiq['illiq'+str(5)] = df['illiq'].rolling(window=5, center=False).mean()
    df_stock_illiq_new = df_stock_illiq.reset_index(drop=True)
    if df_stock_illiq_new.shape[0] != 0:
        pd.DataFrame.to_csv(df_stock_illiq_new, target_dir + os.sep + stock_code + '.csv', encoding='gbk')


df_count = pd.DataFrame()
szlistfile = os.listdir(read_dir_illiq)
for stock_file in szlistfile:
    df_stock_illiq_compare = pd.read_csv(read_dir_illiq + os.sep + stock_file,
                                         usecols=['ts_code', 'trade_date', 'illiq5'])
    #行转列
    df_illiq_transpotion = df_stock_illiq_compare.pivot_table(index='ts_code', columns='trade_date', values='illiq5',
                                                              aggfunc=np.mean)
    df_count = df_count.append(df_illiq_transpotion)
pd.DataFrame.to_csv(df_count, target_dir_illiq + os.sep + 'illiq.csv', encoding='gbk')
'''
df = pd.read_csv(target_dir_illiq + os.sep + 'test.csv')
#df = sc.get_nost_stock(df)
# 取非流动因子文件的前50个股票
df_50 = df[:500]
#print df_50

t = 0
df_colunm_num = df_50.shape[1]
# 分别对每一列日期下的非流动因子大小进行排序
for df_colunm in df_50:
    # 如果第一列为ts_code则跳过不排序
    if str(df_colunm) == 'ts_code':
        continue
    # 分别对每一列进行非流动因子从大到小排序
    else:
        df_sort = df_50.sort_values(by=str(df_colunm), ascending=False, axis=0)
        df_sort_num = df_sort.shape[0]
        start_date = '20190307'
        start_date = dt.strptime(start_date, '%Y%m%d')
        start_date = start_date + d.timedelta(days=t)
        start_date = start_date.strftime('%Y%m%d')
        index_return = sc.get_backward_returns('399001.SZ.csv', start_date, '20190628', 5)
        index_return_1 = index_return[:1]
        # print index_return_1[0]['return5']
        t = t + 1
        for k in range(0, df_sort_num):
            sz_code = df_sort.iloc[k]['ts_code']
            stock_file = sz_code + '.csv'
            df_return = sc.get_backward_returns(stock_file, start_date, '20190628', 5)
            df_illiq_return_1 = df_return[:1]
            return_diff = df_illiq_return_1.iloc[0]['return5'] - index_return_1.iloc[0]['return5']
            # print return_diff
            # print df_illiq_return_1[k]['return5']
            print (start_date, sz_code, index_return_1.iloc[0]['return5'], df_illiq_return_1.iloc[0]['return5'],
                   return_diff)

#print df_sort
        
