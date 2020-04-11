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
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/day_download'
targetdir_week = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/week_download'
targetdir_cap = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/sz_capital'
startdate = '20050101'
#midday = '20100101'
# 得到系统日期的前一天
formatted_yesterday = sc.get_sys_date()
ma_day_list = [20]
ma_week_list = [5]
stock_list = sc.get_sz_stock()
# print stock_list
stock_num = stock_list.shape[0]


df = pd.DataFrame()
#df_frames_week_result = pd.DataFrame()

time_format = dtt.strptime(formatted_yesterday, '%Y%m%d')
weekday = time_format.weekday()


for i in range(0, stock_num):

    stock_code = stock_list.iloc[i]['ts_code']
    #print stock_code
    # print(ts.get_hist_data('000001', start='1991-01-01', end='2019-01-01', ))
    df_day = pd.DataFrame()
    #df_2 = pd.DataFrame()
    df_week = pd.DataFrame()
    #df_week_2 = pd.DataFrame()
    for _ in range(3):
        try:
            df_day = ts.pro_bar(ts_code=stock_code, freq='D', adj='qfq', start_date=startdate, end_date=formatted_yesterday)
            #df_2 = ts.pro_bar(ts_code=stock_code, freq='D', adj='hfq', start_date=midday, end_date=formatted_yesterday)
            if weekday == 5 or weekday == 6:
                df_week = ts.pro_bar(ts_code=stock_code, freq='W', adj='qfq', start_date=startdate, end_date=formatted_yesterday)
                #df_week_2 = ts.pro_bar(ts_code=stock_code, freq='W', adj='hfq', start_date=midday, end_date=formatted_yesterday)

                #print df_week
            #else:
               # df_week = None
        except:
            time.sleep(2)

    #frames = [df_2, df_1]
    #df_frames_result = pd.concat(frames)
    #frames_week = [df_week_2, df_week_1]
    #df_frames_week_result = pd.concat(frames_week)
    if df_day.empty:
        continue

    else:
        #frames = [df_2, df_1]
        #df_frames_result = pd.concat(frames)
        df = df_day.sort_values(by='trade_date', ascending=True)
        for ma in ma_day_list:
            df['MA_' + str(ma)] = round(df['close'].rolling(window=ma, center=False).mean(), 2)
        df_new = df.reset_index(drop=True)
        pd.DataFrame.to_csv(df_new, targetdir + os.sep + stock_code + '.csv', encoding='gbk')
        #rownum = df.shape[0]
        #if rownum == 4000:
            #enddate_mid = int(int(startdate) + int(formatted_yesterday))/2
            #enddate_mid_str = str(enddate_mid)
            #df1 = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=startdate, end_date=enddate_mid_str)

            #df2 = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=enddate_mid_str, end_date=formatted_yesterday)

    if df_week.empty:
        continue
    else:

        df_week_sort = df_week.sort_values(by='trade_date', ascending=True)
        for ma in ma_week_list:
            df_week_sort['MA_' + str(ma)] = round(df_week_sort['close'].rolling(window=ma, center=False).mean() ,2)
        df_week_new = df_week_sort.reset_index(drop=True)
        pd.DataFrame.to_csv(df_week_new, targetdir_week + os.sep + stock_code + '.csv', encoding='gbk')


# 获取深证成分指数日线数据
df_index_1 = pro.index_daily(ts_code='399001.SZ', start_date=startdate, end_date=formatted_yesterday)
#df_index_2 = pro.index_daily(ts_code='399001.SZ', start_date=midday, end_date=formatted_yesterday)
#frames_index = [df_index_2, df_index_1]
#frames_result_index = pd.concat(frames_index)


df_index_week_1 =pro.index_weekly(ts_code='399001.SZ', start_date=startdate, end_date=formatted_yesterday)
#df_index_week_2 =pro.index_weekly(ts_code='399001.SZ', start_date=midday, end_date=formatted_yesterday)
#frames_index_week = [df_index_2, df_index_1]
#frames_result_index_week = pd.concat(frames_index_week)
df_index = df_index_1.sort_values(by='trade_date', ascending=True)
df_index_week = df_index_week_1.sort_values(by='trade_date', ascending=True)
df_index = df_index.reset_index(drop=True)
df_index_week = df_index_week.reset_index(drop=True)
for ma in ma_day_list:
    df_index['MA_' + str(ma)] = df_index['close'].rolling(window=ma, center=False).mean()
    #df_index_week['MA_' + str(ma)] = df_index_week['close'].rolling(window=ma, center=False).mean()
for ma in ma_week_list:
    #df_index['MA_' + str(ma)] = df_index['close'].rolling(window=ma, center=False).mean()
    df_index_week['MA_' + str(ma)] = df_index_week['close'].rolling(window=ma, center=False).mean()
pd.DataFrame.to_csv(df_index, targetdir + os.sep + '399001.SZ.csv', encoding='gbk')
pd.DataFrame.to_csv(df_index_week, targetdir_week + os.sep + '399001.SZ.csv', encoding='gbk')


#取股票市值
trade_date = sc.get_last_trade_day()
#trade_date = '20190822'
df_cap = pro.query('daily_basic',  trade_date=trade_date, fields='ts_code,trade_date,turnover_rate,circ_mv')
pd.DataFrame.to_csv(df_cap, targetdir_cap + os.sep + trade_date + '.csv', encoding='gbk')
