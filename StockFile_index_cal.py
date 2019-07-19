# coding: utf-8
import tushare as ts
import pandas as pd
import os


token = ts.set_token()
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/'
startdate = '19910101'
enddate = '20190705'
ma_list = [5, 10, 20]
pro = ts.pro_api(token)
stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
stock_num = stock_list.shape[0]

for i in range(0, stock_num):

    stock_code = stock_list.iloc[i]['ts_code']
    #print stock_code
    # print(ts.get_hist_data('000001', start='1991-01-01', end='2019-01-01', ))

    df = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=startdate, end_date=enddate)
    # print type(df)
    rownum = df.shape[0]
    # print rownum
    if rownum == 4000:
        enddate_mid = int(int(startdate) + int(enddate))/2
        enddate_mid_str = str(enddate_mid)
        df1 = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=startdate, end_date=enddate_mid_str)

        df2 = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=enddate_mid_str, end_date=enddate)
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

    #pd.DataFrame.to_csv(df, targetdir + os.sep + '000001.csv',  encoding='gbk')
# coding: utf-8
import tushare as ts
import pandas as pd
import os
import stock_class as sc

'''
#通过 tushare的stock_basic、pro_bar、daily_basic接口计算股票总市值、流通市值
@author  by hyq
'''

# 联接tushare的api接口
pro = sc.get_tocken()
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/'
startdate = '19910101'
# 得到系统日期的前一天
formatted_trade_date = sc.get_sys_date()
ma_list = [5, 10, 250]
stock_list = sc.get_sz_stock()
# print stock_list
stock_num = stock_list.shape[0]

for i in range(0, stock_num):

    stock_code = stock_list.iloc[i]['ts_code']
    #print stock_code
    # print(ts.get_hist_data('000001', start='1991-01-01', end='2019-01-01', ))

    df = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=startdate, end_date=formatted_trade_date)
    # print type(df)
    rownum = df.shape[0]
    # print rownum
    if rownum == 4000:
        enddate_mid = int(int(startdate) + int(formatted_trade_date))/2
        enddate_mid_str = str(enddate_mid)
        df1 = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=startdate, end_date=enddate_mid_str)

        df2 = ts.pro_bar(ts_code=stock_code, adj='hfq', start_date=enddate_mid_str, end_date=formatted_trade_date)
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

    #pd.DataFrame.to_csv(df, targetdir + os.sep + '000001.csv',  encoding='gbk')

    
