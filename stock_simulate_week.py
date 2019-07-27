# coding: utf-8
import tushare as ts
import pandas as pd
import os
import csv
import stock_class as sc
import numpy as np

# 联接tushare的api接口
pro = sc.get_tocken()
sys_date = sc.get_sys_date()
trade_days = pro.trade_cal(exchange='', start_date='19910101', end_date=sys_date)
trade_day = trade_days[trade_days['is_open'] == 1]
last_trade_day = trade_day.sort_values('cal_date', ascending=False).head(1)
last_trade_day_value = last_trade_day.iloc[0]['cal_date']


read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare_annual_return/nhsy.csv'
read_dir_week = 'D:/Program Files/tdx/vipdoc/sz/sz_week_fill'
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_week_simulate'
stock_list = pd.read_csv(read_dir, usecols=['ts_code', 'year_annual_return'])
stock_list_5 = stock_list[stock_list['year_annual_return'] >= 0]

stock_num = stock_list_5.shape[0]
for i in range(0, stock_num):
    stock_code = stock_list_5.iloc[i]['ts_code']
    df = ts.pro_bar(ts_code=stock_code,  adj='hfq', start_date=last_trade_day_value, end_date=last_trade_day_value)
    df_day = pd.DataFrame(df, columns=['ts_code', 'close'])
    read_dir_week_files = os.listdir(read_dir_week)
    for stock_file in read_dir_week_files:
        if stock_file == (stock_code + '.csv'):
            df_week = pd.read_csv(read_dir_week + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'close', 'open',
                                                                           'high', 'low', 'pre_close', 'change',
                                                                           'pct_chg', 'vol', 'amount', 'ma5', 'ma_v_5',
                                                                           'flag'])
            df_union = pd.concat([df_week, df_day], axis=0, sort=False)
            df_union_new = df_union.reset_index(drop=True)
            row_num = df_union_new.shape[0]
            j = 5
            week_ma_5 = 0
            while j > 0:
                week_ma_5 = df_union_new.iloc[row_num-1]['close'] + week_ma_5
                j = j-1
                row_num = row_num - 1
            ma5 = round(week_ma_5/5, 2)
            row_num = df_union_new.shape[0]
            df_union_new.at[row_num-1, 'ma5'] = ma5
            mask = df_union_new.iloc[row_num - 1]['close'] - df_union_new.iloc[row_num - 1]['ma5']
            if mask > 0:
                df_union_new.at[row_num - 1, 'flag'] = 1
            elif mask < 0:
                df_union_new.at[row_num - 1, 'flag'] = 0
            else:
                continue
            if (df_union_new.iloc[row_num - 1]['flag'] == 1) and (df_union_new.iloc[row_num - 2]['flag'] == 0):
                print stock_code

            pd.DataFrame.to_csv(df_union_new, target_dir + os.sep + stock_code + '.csv', encoding='gbk')

