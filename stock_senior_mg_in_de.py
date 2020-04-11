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
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/senior_mg_in_de'
targetdir_week = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/week_download'
targetdir_cap = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/sz_capital'
startdate = '19910101'
midday = '20150101'

'''
df = ts.pro_bar(ts_code='000034.SZ', adj='hfq', start_date='20000101', end_date='20200403')
print(df)
'''


pro = sc.get_tocken()

stock_list = sc.get_sz_stock()
stock_num = stock_list.shape[0]
for i in range(0, stock_num):
    stock_code = stock_list.iloc[i]['ts_code']
    df = pro.stk_holdertrade(ts_code=stock_code, fields='ts_code,ann_date,holder_name,holder_type,in_de,change_vol,'
                                                         'change_ratio,after_share,after_ratio,total_share,begin_date,'
                                                         'close_date')
    pd.DataFrame.to_csv(df, target_dir + os.sep + stock_code + '.csv', encoding='gbk')


