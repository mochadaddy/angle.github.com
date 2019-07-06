# coding: utf-8
import tushare as ts
import pandas as pd
import os


token = ts.set_token('71a5947e1d01e9b5c5275f2de127101940acd4cdb44cc2aad9c7e7cd')

pro = ts.pro_api(token)
# print(ts.get_hist_data('000001', start='1991-01-01', end='2019-01-01', ))
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/'

#data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

startdate = '19910101'
enddate = '20190501'
df = ts.pro_bar(ts_code='000001.SZ', adj='hfq', start_date=startdate, end_date=enddate)
# print type(df)
rownum = df.shape[0]
print rownum
if rownum == 4000:
    enddate_mid = int(int(startdate) + int(enddate))/2
    enddate_mid_str = str(enddate_mid)
    df1 = ts.pro_bar(ts_code='000001.SZ', adj='hfq', start_date=startdate, end_date=enddate_mid_str)

    df2 = ts.pro_bar(ts_code='000001.SZ', adj='hfq', start_date=enddate_mid_str, end_date=enddate)
    frames = [df2, df1]
    frames_result = pd.concat(frames)
    df = frames_result.sort_values('trade_date', ascending=True)
    print (df)
    pd.DataFrame.to_csv(df, targetdir + os.sep + '000001.csv',  encoding='gbk')




#pd.DataFrame.to_csv(df, targetdir + os.sep + '000001.csv',  encoding='gbk')







