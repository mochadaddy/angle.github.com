# coding: utf-8
'''
计算从上市日到去年年底的股票年化收益率

'''
import tushare as ts
import pandas as pd
import os
import csv
import stock_class as sc


pro = sc.get_tocken()
sys_day = sc.get_sys_date()
# stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
stock_list_sz = sc.get_sz_stock()
stock_sz_num = stock_list_sz.shape[0]
stock_analyse_capital = pd.DataFrame(index=range(0, stock_sz_num), columns=['ts_code', 'year', 'year_annual_return'])
# print stock_list_sz
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare_annual_return'
szpathdir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare'
szlistfile = os.listdir(szpathdir)
j = 0
for stock_file in szlistfile:
    # print stock_file
    df = pd.read_csv(szpathdir + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'open', 'close', 'pct_chg',
                                                               'vol', 'amount', 'MA_5', 'MA_10', 'MA_250'])

    end_date = '20181228'
    start_date = df.iloc[0]['trade_date']
    start_date_close = df.iloc[0]['close']
    start_date_int = int(start_date)
    start_date_str = str(start_date_int)
    end_date_q4 = end_date[0:4]
    start_date_str_q4 = start_date_str[0:4]
    year_num = int(end_date_q4) - int(start_date_str_q4)
    row_num = df.shape[0]
    if row_num >= 500:
        for i in range(0, row_num):
            date_int_2019 = int(df.iloc[i]['trade_date'])
            date_int_2018 = int(df.iloc[i - 1]['trade_date'])
            date_str_2019 = str(date_int_2019)
            date_str_2018 = str(date_int_2018)
            date_str_2019_q4 = date_str_2019[0:4]
            date_str_2018_q4 = date_str_2018[0:4]
            if (date_str_2019_q4 == '2019') and (date_str_2018_q4 == '2018'):
                code = df.iloc[i]['ts_code']
                close_2018 = df.iloc[i - 1]['MA_250']
                annual_return = (close_2018 - start_date_close) / year_num
                annual_return_tmp = round(annual_return, 2)
                # df.loc[i - 1, 'annual_return'] = annual_return_tmp
                stock_analyse_capital.at[stock_analyse_capital.index[j], 'ts_code'] = code
                stock_analyse_capital.at[stock_analyse_capital.index[j], 'year'] = date_str_2018_q4
                stock_analyse_capital.at[stock_analyse_capital.index[j], 'year_annual_return'] = annual_return_tmp
                j = j+1
                print code
                print annual_return_tmp

pd.DataFrame.to_csv(stock_analyse_capital, targetdir + os.sep + sys_day + 'nhsy.csv', encoding='gbk')


    
