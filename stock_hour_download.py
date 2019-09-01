# coding: utf-8
import tushare as ts
import pandas as pd
import os
import stock_class as sc
import time
import datetime as dt
from datetime import datetime as dtt

'''
#通过 tushare的stock_basic、pro_bar、daily_basic接口计算股票总市值、流通市值
@author  by hyq
'''

# 联接tushare的api接口
pro = sc.get_tocken()
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/hour_download'
targetdir_week = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/week_download'
targetdir_cap = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/sz_capital'
startdate = '19910101'
# 得到系统日期的前一天
formatted_yesterday = sc.get_sys_date()
ma_list = [5, 10, 250]
stock_list = sc.get_sz_stock()
# print stock_list
stock_num = stock_list.shape[0]

df_hour = pd.DataFrame()

time_format = dtt.strptime(formatted_yesterday, '%Y%m%d')
weekday = time_format.weekday() + 1

for i in range(0, stock_num):

    stock_code = stock_list.iloc[i]['ts_code']
    # print stock_code
    # print(ts.get_hist_data('000001', start='1991-01-01', end='2019-01-01', ))

    for _ in range(3):
        try:
            #df = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=startdate, end_date=formatted_yesterday)
            df_hour = ts.pro_bar(ts_code=stock_code, adj='hfq', freq='60min', start_date='20190731', end_date='20190831')


        except:
            time.sleep(2)
    if df_hour is None:
        continue

    pd.DataFrame.to_csv(df_hour, target_dir + os.sep + stock_code + '.csv', encoding='gbk')

