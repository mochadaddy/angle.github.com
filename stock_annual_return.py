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
szpathdir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/day_download'
szlistfile = os.listdir(szpathdir)
file_count = 0
j = 0
for stock_file in szlistfile:
    # print stock_file
    file_count = file_count + 1
    df = pd.read_csv(szpathdir + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'open', 'close', 'pct_chg',
                                                               'vol', 'amount', 'MA_5', 'MA_10', 'MA_250'])


    row_num = df.shape[0]
    if row_num >= 500:
        year_num = round(row_num / 250, 2)
        return_sum = df.iloc[row_num - 1]['close'] - df.iloc[0]['close']
        annual_return = round(return_sum / df.iloc[0]['close']/year_num, 2)
        code = df.iloc[0]['ts_code']
        end_date = df.ix[row_num-1, 'trade_date']
        #print (code, end_date, annual_return, return_sum, row_num, year_num,)
        stock_analyse_capital.at[stock_analyse_capital.index[j], 'ts_code'] = code
        stock_analyse_capital.at[stock_analyse_capital.index[j], 'year'] = end_date
        stock_analyse_capital.at[stock_analyse_capital.index[j], 'year_annual_return'] = annual_return
        j = j + 1
pd.DataFrame.to_csv(stock_analyse_capital, targetdir + os.sep + 'nhsy.csv', encoding='gbk')



    
