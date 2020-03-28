# coding: utf-8
import tushare as ts
import pandas as pd
import os
import stock_class as sc
import time
import datetime as dt
from datetime import datetime as dtt



pro = sc.get_tocken()
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/firstday_download_sz'
startdate = '19910701'


#print format_next_day
format_next_day = '19910701'
stock_list = sc.get_sz_stock()
stock_num = stock_list.shape[0]
num = 0
flag = True
for i in range(0, stock_num):
    stock_code = stock_list.iloc[i]['ts_code']


    #for _ in range(3):
        #try:
    row_num = 0

    while row_num == 0:
        for _ in range(3):
            try:
                df = pd.DataFrame(ts.pro_bar(ts_code=stock_code, freq='D', adj='hfq', start_date=startdate, end_date=format_next_day))
                row_num = df.shape[0]
                #if df.empty is True:
                if row_num == 0:
                    format_startdate = dtt.strptime(startdate, '%Y%m%d')
                    num = num + 1
                    next_day = format_startdate + dt.timedelta(days=num)
                    format_next_day = next_day.strftime('%Y%m%d')
                else:
                    if row_num == 1:
                        pd.DataFrame.to_csv(df, target_dir + os.sep + stock_code + '.csv', encoding='gbk')
                        break
                    else:
                        df = df[0:1]
                        pd.DataFrame.to_csv(df, target_dir + os.sep + stock_code + '.csv', encoding='gbk')
                        break

            except:
                time.sleep(2)





        #except:
            #time.sleep(2)


