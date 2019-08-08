# coding: utf-8
import tushare as ts
import pandas as pd
import os
import stock_class as sc
import time

'''
#通过 tushare的stock_basic、pro_bar、daily_basic接口计算股票总市值、流通市值
@author  by hyq
'''

# 联接tushare的api接口
pro = sc.get_tocken()
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/day_download'
targetdir_week = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/week_download'
startdate = '19910101'
# 得到系统日期的前一天
formatted_yesterday = sc.get_sys_date()
ma_list = [5, 10, 250]
stock_list = sc.get_sz_stock()
# print stock_list
stock_num = stock_list.shape[0]

df = pd.DataFrame()
df_week = pd.DataFrame()

for i in range(280, stock_num):

    stock_code = stock_list.iloc[i]['ts_code']
    #print stock_code
    # print(ts.get_hist_data('000001', start='1991-01-01', end='2019-01-01', ))

    for _ in range(3):
        try:
            df = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=startdate, end_date=formatted_yesterday)
            df_week = ts.pro_bar(ts_code=stock_code, freq='W', adj='hfq', start_date=startdate,
                                 end_date=formatted_yesterday,
                                 ma=[5])
        except:
            time.sleep(2)
    if df is None:
        continue
    else:
        rownum = df.shape[0]
        if rownum == 4000:
            enddate_mid = int(int(startdate) + int(formatted_yesterday))/2
            enddate_mid_str = str(enddate_mid)
            df1 = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=startdate, end_date=enddate_mid_str)

            df2 = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=enddate_mid_str, end_date=formatted_yesterday)
            if df1 is None or df2 is None:
                continue
            else:
                frames = [df2, df1]
                frames_result = pd.concat(frames)
                df = frames_result.sort_values('trade_date', ascending=True)
                # df = df.sort_values('trade_date', ascending=True)
                for ma in ma_list:
                    df['MA_' + str(ma)] = df['close'].rolling(window=ma, center=False, ).mean()
                # print (df)
                df_new = df.reset_index(drop=True)
                pd.DataFrame.to_csv(df_new, targetdir + os.sep + stock_code + '.csv',  encoding='gbk')
        else:
            df = df.sort_values('trade_date', ascending=True)
            for ma in ma_list:
                df['MA_' + str(ma)] = df['close'].rolling(window=ma, center=False, ).mean()
            df_new = df.reset_index(drop=True)
            pd.DataFrame.to_csv(df_new, targetdir + os.sep + stock_code + '.csv', encoding='gbk')

        df_week_sort = df_week.sort_values('trade_date', ascending=True)
        pd.DataFrame.to_csv(df_week_sort, targetdir_week + os.sep + stock_code + '.csv', encoding='gbk')
    #pd.DataFrame.to_csv(df, targetdir + os.sep + '000001.csv',  encoding='gbk')
'''
# 获取深证成分指数日线数据
df_index = pro.index_daily(ts_code='399001.SZ', start_date=startdate, end_date=formatted_yesterday)
df_index = df_index.sort_values('trade_date', ascending=True)
df_index = df_index.reset_index(drop=True)
for ma in ma_list:
    df_index['MA_' + str(ma)] = df_index['close'].rolling(window=ma, center=False, ).mean()
pd.DataFrame.to_csv(df_index, targetdir + os.sep + '399001.SZ.csv', encoding='gbk')


''' 
