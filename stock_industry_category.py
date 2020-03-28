# coding: utf-8
import tushare as ts
import pandas as pd
import os
import stock_class as sc
import re
import json
import time

import datetime as dt
from datetime import datetime as dtt


#type = sys.getfilesystemencoding()
pro = sc.get_tocken()
#df_industry_category = pd.DataFrame()
#target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/day_downloadD:/Program Files/tdx/vipdoc/sz/sz_tushare/day_download'
read_dir = 'D:/Program Files/tdx/vipdoc/sz/industry_category'
target_dir = 'D:/Program Files/tdx/vipdoc/sz/industry_category/stock_category'
df_stock_industry_category = pd.read_csv(read_dir + os.sep + 'stock_category_L3.csv', usecols=['index_code', 'industry_name', 'level'], encoding='gbk')
row_num = df_stock_industry_category.shape[0]
for i in range(0, row_num):
    for _ in range(3):
        try:
            df = pro.index_member(index_code=df_stock_industry_category.iloc[i]['index_code'], fields='index_code,con_code,in_date,out_date,is_new')
            row_num_industry = df.shape[0]
        except:
            time.sleep(2)

        df_industry_category = pd.DataFrame()
        for j in range(0,row_num_industry):
            if df.iloc[j]['con_code'].endswith('SZ') is True:
                df_industry_category.at[j,''] = df.iloc[j]['index_code']
                df_industry_category.at[j, 'con_code'] = df.iloc[j]['con_code']
                df_industry_category.at[j, 'index_name'] = df_stock_industry_category.iloc[i]['industry_name']
            df_industry_category_new = df_industry_category.reset_index(drop=True)
    pd.DataFrame.to_csv(df_industry_category_new, target_dir + os.sep + 'test.csv', mode='ab', header=False, encoding='gbk')

