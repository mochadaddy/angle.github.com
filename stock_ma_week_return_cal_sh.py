# coding: utf-8
'''
根据标志位得到买入卖出价格，并计算策略收益、资金曲线、最大回撤比例。并与未采用策略的年化收益比较，得出使用
策略的优劣
'''
import pandas as pd
import numpy as np
import os
import glob
import stock_class as sc



target_dir = 'D:/Program Files/tdx/vipdoc/sh/sh_week_return'
read_dir = 'D:/Program Files/tdx/vipdoc/sh/sh_week_fill'
target_dir_conclude = 'D:/Program Files/tdx/vipdoc/sh/sh_week_conclude'
fileNames_week = glob.glob(target_dir + r'\*')
before_20_year_day = sc.get_20_years_day()

for fileName in fileNames_week:
    try:
        os.remove(fileName)
    except:
        break
m = n = q = 0
df_ma_conclude = pd.DataFrame()
read_dir_files = os.listdir(read_dir)
for stock_file in read_dir_files:
    q = q + 1
    df = pd.read_csv(read_dir + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'close', 'ma5', 'flag'])
    df_mid = df[df['trade_date'] >= before_20_year_day]
    df_new = df_mid.reset_index(drop=True)
    row_num = df_new.shape[0]
    buy_price = None
    k = 0
    o = p = 0
    positive_return = negative_return = 0
    year_num = round(row_num * 1.00 / 52, 2)
    for i in range(1, row_num):

    # 当标志位从0变为1时，记录买入价格，当标志位从1变为0时，记录卖出价格，从买入卖出价格计算本次买卖收益率


        if np.isnan(df_new.iloc[i]['ma5']):
            continue
        else:
            if df_new.iloc[i - 1]['flag'] == 0 and df_new.iloc[i]['flag'] == 1:
                buy_price = df_new.iloc[i]['close']
                k = k + 1
                # 初始化买入价格，历史最高价格，回撤比例
                if k == 1:
                    df_new.at[i, 'money_cal'] = df_new.iloc[i]['close']
                    buy_price_init = df_new.iloc[i]['close']
                    max_price = buy_price_init
                    max_withdrawal_rate = 0
            if df_new.iloc[i - 1]['flag'] == 1 and df_new.iloc[i]['flag'] == 0:
                if buy_price is None:
                    continue
                else:
                    sell_price = df_new.iloc[i]['close']
                    return_rate = (sell_price - buy_price) / buy_price
                    if return_rate > 0:
                        o = o + 1
                        positive_return = return_rate + positive_return

                    if return_rate < 0:
                        p = p + 1
                        negative_return = return_rate + negative_return

                    df_new.at[i, 'return_rate'] = return_rate
                    j = i
                    while pd.isnull(df_new.iloc[j]['money_cal']):
                        j = j - 1
                    df_new.at[i, 'money_cal'] = df_new.iloc[j]['money_cal'] * return_rate + df_new.iloc[j]['money_cal']
                    # 取得当前价格之前的最高价格
                    if df_new.iloc[i]['money_cal'] > max_price:
                        max_price = df_new.iloc[i]['money_cal']
                    # 计算最大回撤比例
                    withdrawal_rate = 1 - (df_new.iloc[i]['money_cal'] / max_price)
                    # 比较所有的回撤比例，取得最大的回撤比例
                    if max_withdrawal_rate < withdrawal_rate:
                        max_withdrawal_rate = round(withdrawal_rate, 4)
                    # 计算策略年化收益率及资金曲线和股票本身年化收益率
                    times = round((df_new.iloc[i]['money_cal']-buy_price_init)/buy_price_init/year_num, 2)
                    times_no_ma5 = round((df_new.iloc[i]['close']-buy_price_init)/buy_price_init/year_num, 2)
    # 评价策略优劣
    if max_withdrawal_rate == 0:
        continue
    else:
        strategy_estimate = round(times/(max_withdrawal_rate*100), 4)
    # 计算盈亏收益比
    positive_return_average = positive_return / o
    negative_return_average = negative_return / p
    profit_to_loss_ratio = round(positive_return_average/abs(negative_return_average), 2)
    win_ratio = round(float(o) / float((o + p)), 2)
    df_ma_conclude.at[q, 'sz_code'] = stock_file[:9]
    df_ma_conclude.at[q, 'times'] = times
    df_ma_conclude.at[q, 'times_no_ma5'] = times_no_ma5
    df_ma_conclude.at[q, 'withdrawal'] = max_withdrawal_rate
    df_ma_conclude.at[q, 'strategy_estimate'] = strategy_estimate
    df_ma_conclude.at[q, 'profit_to_loss_ratio'] = profit_to_loss_ratio
    df_ma_conclude.at[q, 'win_ratio'] = win_ratio
    #print (stock_file, times, times_no_ma5, max_withdrawal_rate, strategy_estimate, profit_to_loss_ratio, win_ratio)
    # 比较采用5周均线策略年化收益和未采用策略的优劣
    if times > times_no_ma5:
        m = m + 1
    else:
        n = n + 1
    pd.DataFrame.to_csv(df_new, target_dir + os.sep + stock_file, encoding='gbk')
pd.DataFrame.to_csv(df_ma_conclude, target_dir_conclude + os.sep + 'conclude.csv', encoding='gbk')
print (m, n)

