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
import time
from datetime import datetime as dt
import datetime as d


read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/hour_download'
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq_hour'
stock_list = sc.get_return_rate(0)
stock_num = stock_list.shape[0]


fileNames_illiq = glob.glob(target_dir + r'\*')
for fileName in fileNames_illiq:
    try:
        os.remove(fileName)
    except:
        break
for j in range(0, stock_num):
    stock_code = stock_list.iloc[j]['ts_code']
    if os.path.exists(read_dir + os.sep + stock_code + '.csv') and stock_code != '399001.SZ':
        #df = ts.pro_bar(ts_code='000001.SZ', adj='hfq', freq='60min', start_date='20190101', end_date='20190830')
        df = pd.read_csv(read_dir + os.sep + stock_code + '.csv', usecols=['ts_code', 'trade_time', 'open', 'high', 'low', 'close', 'amount'])

        row_num = df.shape[0]
        illiq_sum = 0
        df_illiq = pd.DataFrame()

        for i in range(0,row_num):
            date_no_format = df.iloc[i]['trade_time']
            #date_no_format_sub = date_no_format
            #print date_no_format_sub
            date_format = dt.strptime(date_no_format, '%Y-%m-%d %H:%M:%S')
            date_format = date_format.strftime('%Y%m%d%H%M')
            date_format_sub = date_format[:8]
            #print date_format_sub
            #print date_format
            illiq = (2*(df.iloc[i]['high'] - df.iloc[i]['low'])-abs(df.iloc[i]['open']-df.iloc[i]['close']))*1.0/df.iloc[i]['amount']*10000000
            #print (date_format,illiq)
            date_format_pre_sub = date_format_sub
            if i > 0:
                date_no_format_pre = df.iloc[i-1]['trade_time']
                date_format_pre = dt.strptime(date_no_format_pre, '%Y-%m-%d %H:%M:%S')
                date_format_pre = date_format_pre.strftime('%Y%m%d%H%M')
                date_format_pre_sub = date_format_pre[:8]

            #date_format_sub_pre = date_format_sub

            if date_format_sub == date_format_pre_sub:
                illiq_sum = illiq + illiq_sum
                df.at[i,'illiq_sum'] = illiq_sum
            else:
                df_illiq.at[i - 1, 'ts_code'] = df.iloc[i]['ts_code']
                df_illiq.at[i - 1, 'date'] = date_format_sub
                df_illiq.at[i - 1, 'illiq'] = illiq_sum

                print (date_format_pre_sub, illiq_sum, )
                illiq_sum = illiq
        df_illiq = df_illiq.sort_values('date', ascending=True)
        df_illiq['illiq' + str(5)] = df_illiq['illiq'].rolling(window=5, center=False).mean()
        df_stock_illiq_new = df_illiq.reset_index(drop=True)

        pd.DataFrame.to_csv(df_stock_illiq_new, target_dir + os.sep + stock_code + '.csv', encoding='gbk')







'''
df = sc.get_stock_cap('000028.SZ', '20190813')
#df = df.sort_values(by='ts_code', ascending=True)
#df = df.reset_index(drop=True)
#row_num = df.shape[0]
print df
illiq_neutrilize = np.log10(df.iloc[0]['circ_mv'])
print illiq_neutrilize

target_dir_cap = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/sz_capital'
pro = sc.get_tocken()
df_cap = pro.query('daily_basic',  trade_date='20190809', fields='ts_code,trade_date,turnover_rate,circ_mv')
pd.DataFrame.to_csv(df_cap, target_dir_cap + os.sep + '20190809' + '.csv', encoding='gbk')


df_new = pd.DataFrame()

target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/sz_detail'
pro = sc.get_tocken()
t = 1
start_date = '2018-12-28'
end_date = '2019-02-22'
#end_date = dt.strptime(end_date, '%Y-%m-%d')
while start_date <= end_date:
    start_date = dt.strptime(start_date, '%Y-%m-%d')
    start_date = start_date + d.timedelta(days=t)

    start_date = start_date.strftime('%Y-%m-%d')
    df_new = ts.get_tick_data('002587', date=start_date, src='tt')
    if df_new is None:
        continue
    else:
    #print df_new

        pd.DataFrame.to_csv(df_new, target_dir + os.sep + start_date + '-002587.csv', encoding='gbk')
    #start_date = start_date.strftime('%Y%m%d')




'''