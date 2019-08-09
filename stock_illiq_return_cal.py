# coding: utf-8
'''
按照日线计算emv指标和maemv指标
'''

import pandas as pd
import os
import numpy as np

from datetime import datetime as dt
import datetime as d

import stock_class as sc


pro = sc.get_tocken()
read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/day_download'
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq'
read_dir_illiq = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq'
target_dir_illiq = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq_compare'
start_date = '20190726'
end_date = '20190801'
stock_list = sc.get_return_rate(0)
stock_num = stock_list.shape[0]

df = pd.read_csv(target_dir_illiq + os.sep + 'no_st.csv')
#df = sc.get_nost_stock(df)
# 取非流动因子文件的前50个股票
df_50 = df
#print df_50

t = 0
df_colunm_num = df_50.shape[1]
# 分别对每一列日期下的非流动因子大小进行排序

for colunm in df_50:
    # 如果第一列为ts_code则跳过不排序
    #print colunm
    if str(colunm) >= start_date and str(colunm) <= end_date:
        df_sort = df_50.sort_values(by=str(colunm), ascending=False, axis=0)
        df_sort_num = df_sort.shape[0]
        start_date = dt.strptime(start_date, '%Y%m%d')
        start_date = start_date + d.timedelta(days=t)
        start_date = start_date.strftime('%Y%m%d')
        index_return = sc.get_backward_returns('399001.SZ.csv', start_date, end_date, 5)
        index_return_1 = index_return[:1]
        # print index_return_1[0]['return5']
        t = t + 1
        for k in range(0, df_sort_num):
            sz_code = df_sort.iloc[k]['ts_code']
            stock_file = sz_code + '.csv'
            df_return = sc.get_backward_returns(stock_file, start_date, end_date, 5)
            df_illiq_return_1 = df_return[:1]
            return_diff = round(df_illiq_return_1.iloc[0]['return5'] - index_return_1.iloc[0]['return5'], 5)

            # print return_diff
            # print df_illiq_return_1[k]['return5']
            print (start_date, sz_code, round(index_return_1.iloc[0]['return5'],5),
                   round(df_illiq_return_1.iloc[0]['return5'], 5), return_diff)
    else:
        continue
#print df_sort




