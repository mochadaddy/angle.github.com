# coding: utf-8
import tushare as ts
import pandas as pd
import os
import csv

df = pd.read_csv('D:/Program Files/tdx/vipdoc/sz/sz_tushare/000001.SZ.csv', usecols=['ts_code', 'trade_date', 'open',
                                                                                     'close', 'pct_chg', 'vol',
                                                                                     'amount', 'MA_5', 'MA_10',
                                                                                     'MA_20'])
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/'
# df['annual_return'] = 0
end_date = '20181228'
start_date = df.iloc[0]['trade_date']
start_date_close = df.iloc[0]['close']
start_date_int = int(start_date)
start_date_str = str(start_date_int)
end_date_q4 = end_date[0:4]
start_date_str_q4 = start_date_str[0:4]
year_num = int(end_date_q4)-int(start_date_str_q4)
row_num = df.shape[0]
for i in range(0, row_num):
    date_int_2019 = int(df.iloc[i]['trade_date'])
    date_int_2018 = int(df.iloc[i-1]['trade_date'])
    date_str_2019 = str(date_int_2019)
    date_str_2018 = str(date_int_2018)
    date_str_2019_q4 = date_str_2019[0:4]
    date_str_2018_q4 = date_str_2018[0:4]
    if (date_str_2019_q4 == '2019')and (date_str_2018_q4 == '2018'):
        close_2018 = df.iloc[i-1]['close']
        annual_return = (close_2018 - start_date_close)/year_num
        annual_return_tmp = round(annual_return, 2)
        df.loc[i-1, 'annual_return'] = annual_return_tmp

pd.DataFrame.to_csv(df, targetdir + os.sep + '000001.SZ.csv', encoding='gbk')

