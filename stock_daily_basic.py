# coding: utf-8
'''
计算从上市日到去年年底的股票年化收益率
'''
import tushare as ts
import pandas as pd
import os
import csv
import stock_class as sc
import time


pro = sc.get_tocken()
stock_list = sc.get_sz_stock()
stock_num = stock_list.shape[0]
formatted_yesterday = sc.get_sys_date()
startdate = '19910101'
midday = '20050101'
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/daily_basic'

for i in range(0, stock_num):
    stock_code = stock_list.iloc[i]['ts_code']
    df1_basic = pd.DataFrame()
    df2_basic = pd.DataFrame()
    for _ in range(3):
        try:
            df1_basic = pro.daily_basic(ts_code=stock_code,  start_date=startdate, end_date=midday)
            df2_basic = pro.daily_basic(ts_code=stock_code,  start_date=midday, end_date=formatted_yesterday)

        except:
            time.sleep(2)

    frames = [df2_basic, df1_basic]
    df_frames_result = pd.concat(frames)
    if df_frames_result.empty:
       continue
    else:
        df = df_frames_result.sort_values(by='trade_date', ascending=True)
    pd.DataFrame.to_csv(df, targetdir + os.sep + stock_code + '.csv', encoding='gbk')




