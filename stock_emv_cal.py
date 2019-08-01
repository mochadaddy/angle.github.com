# coding: utf-8
'''
按照日线计算emv指标和maemv指标

'''
import tushare as ts
import pandas as pd
import os
import glob
import csv
import stock_class as sc
import numpy as np


def cal_return(df, ma_emv, emv):
    row_num = df.shape[0]
    # df['flag'] = -1
    k = 0
    buy_price = None
    # df['em'] = 0
    #df['EMV'] = 0
    #df['MA_EMV' + str(ma_emv)] = 0
    for i in range(0, row_num):
        price_high_i = df.ix[i, 'high']
        price_low_i = df.ix[i, 'low']
        amount = df.ix[i, 'amount'] / 10
        if i > 0:
            price_high_i_last_day = df.ix[i - 1, 'high']
            price_low_i_last_day = df.ix[i - 1, 'low']
            em = ((price_high_i + price_low_i) / 2 - (price_high_i_last_day - price_low_i_last_day) / 2) * (
                    price_high_i - price_low_i) / amount
            df.at[i, 'em'] = em
            df['EMV' + str(emv)] = df['em'].rolling(window=emv, center=False).mean()
            df['MA_EMV' + str(ma_emv) + str(emv)] = df['EMV' + str(emv)].rolling(window=ma_emv, center=False, ).mean()
            # df['MA_EMV'] = df['EMV'].rolling(window=10, center=False).mean()

            if df.iloc[i]['EMV' + str(emv)] > df.iloc[i]['MA_EMV' + str(ma_emv) + str(emv)]:
                df.at[i, 'flag' + str(ma_emv) + str(emv)] = 1
            if df.iloc[i]['EMV' + str(emv)] < df.iloc[i]['MA_EMV' + str(ma_emv) + str(emv)]:
                df.at[i, 'flag' + str(ma_emv) + str(emv)] = 0
            if df.iloc[i]['EMV' + str(emv)] == df.iloc[i]['MA_EMV' + str(ma_emv) + str(emv)]:
                df.at[i, 'flag' + str(ma_emv) + str(emv)] = -1
            # print (i, round(df.iloc[i]['em'], 6), round(df.iloc[i]['EMV'], 6), round(df.iloc[i]['MA_EMV'], 6), )
            if np.isnan(df.iloc[i]['MA_EMV' + str(ma_emv) + str(emv)]):
                continue
            else:
                if df.iloc[i]['flag' + str(ma_emv) + str(emv)] is None:
                    continue
                if df.iloc[i - 1]['flag' + str(ma_emv) + str(emv)] == 0 and df.iloc[i]['flag' + str(ma_emv) + str(emv)] == 1:
                    buy_price = df.iloc[i]['close']
                    #print (i, buy_price)

                    k = k + 1
                    # 初始化买入价格，历史最高价格，回撤比例
                    if k == 1:
                        df.ix[i, 'money_cal' + str(ma_emv) + str(emv)] = df.ix[i, 'close']
                        #buy_price_init = df.ix[i, 'close']
                        #max_price = buy_price_init
                        #max_withdrawal_rate = 0
                if df.iloc[i - 1]['flag' + str(ma_emv) + str(emv)] == 1 and df.iloc[i]['flag' + str(ma_emv) + str(emv)] == 0:
                    if buy_price is None:
                        continue
                    else:
                        sell_price = df.iloc[i]['close']
                        #print (i, sell_price)
                        return_rate = (sell_price - buy_price) / buy_price
                        #print (i, return_rate)
                        # print (i, return_rate)
                        j = i
                        while pd.isnull(df.iloc[j]['money_cal' + str(ma_emv) + str(emv)]):
                            j = j - 1
                        df.ix[i, 'money_cal' + str(ma_emv) + str(emv)] = df.ix[j, 'money_cal' + str(ma_emv) + str(emv)] * return_rate + df.ix[j, 'money_cal' + str(ma_emv) + str(emv)]

                        df.at[i, 'return_rate' + str(ma_emv) + str(emv)] = return_rate
    return df

# 联接tushare的api接口
pro = sc.get_tocken()
yesterday = sc.get_sys_date()

read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/day_download'
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_emv_cal'

df = pd.read_csv(read_dir + os.sep + '300691.SZ.csv', usecols=['ts_code', 'trade_date', 'open', 'high', 'low', 'close',
                                                               'pct_chg', 'vol', 'amount', 'MA_5', 'MA_10', 'MA_250'])

maemv_list = [10, 15, 20]
emv_list = [5, 7, 9]
for ma_emv in maemv_list:
    for emv in emv_list:
        cal_return(df, ma_emv, emv)
        pd.DataFrame.to_csv(df, target_dir + os.sep + '300691.csv', encoding='gbk')

                #print (i, round(df.iloc[i]['EMV'], 6), round(df.iloc[i]['MA_EMV'], 6), buy_price, sell_price,
                       #return_rate)



