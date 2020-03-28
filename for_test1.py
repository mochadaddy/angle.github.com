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
startdate = '19910101'
midday = '20150101'


df_1 = pd.DataFrame(ts.pro_bar(ts_code='000001.SZ', freq='D', adj='hfq', start_date=startdate, end_date=midday))
print(df_1)
