# coding: utf-8
import tushare as ts
import pandas as pd
import os
import csv
import stock_class as sc


def find_win_team(df_new):
    winners = []
    for i, row in df.iterrows():
        if row['score_A'] > row['score_B']:
            winners.append(row['team_A'])
        elif row['score_A'] < row['score_B']:
            winners.append(row['team_B'])
        else:
            winners.append('Draw')
    return winners



# 联接tushare的api接口
pro = sc.get_tocken()
yestorday = sc.get_sys_date()
targetdir = 'D:/Program Files/tdx/vipdoc/sz/sz_week'
df = ts.pro_bar(ts_code='000001.SZ', freq='W', adj='hfq', start_date='19910101', end_date=yestorday, ma=[5])
df_aes = df.sort_values('trade_date', ascending=True)
df_new = df_aes.reset_index(drop=True)
df_new['flag'] = None
row_num = df_new.shape[0]
print df_new

for i in range(0, row_num):
    if df_new.iloc[i]['close'] >= df_new.iloc[i]['ma5']:
        df_new.iloc[i]['flag'] = 1
    if df_new.iloc[i]['close'] < df_new.iloc[i]['ma5']:
        df_new.iloc[i]['flag'] = 0



pd.DataFrame.to_csv(df_new, targetdir + os.sep + '000001.csv', encoding='gbk')
