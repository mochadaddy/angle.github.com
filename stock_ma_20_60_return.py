# coding: utf-8
'''
根据标志位得到买入卖出价格，并计算策略收益、资金曲线、最大回撤比例。并与未采用策略的年化收益比较，得出使用
策略的优劣
'''
import pandas as pd
import numpy as np
import os
import glob


target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_ma_20_60_return'
read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_ma_20_60_stategy_fill'
target_dir_conclude = 'D:/Program Files/tdx/vipdoc/sz/sz_ma_20_60_conclude'
fileNames_ma_20_60 = glob.glob(target_dir + r'\*')

for fileName in fileNames_ma_20_60:
    try:
        os.remove(fileName)
    except:
        break

m = n = q = 0
df_ma_20_60_conclude = pd.DataFrame()
read_dir_files = os.listdir(read_dir)
for stock_file in read_dir_files:
    q = q + 1
    df = pd.read_csv(read_dir + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'close', 'MA_20', 'flag'])
    row_num = df.shape[0]
    buy_price = None
    year_num = round(row_num * 1.00 / 250, 2)
    k = 0
    o = p = 0
    positive_return = negative_return = 0
    #times = max_withdrawal_rate = max_price = 0
    # 当标志位从0变为1时，记录买入价格，当标志位从1变为0时，记录卖出价格，从买入卖出价格计算本次买卖收益率
    for i in range(0, row_num):
        if np.isnan(df.iloc[i]['MA_20']):
            continue
        else:
            if df.iloc[i - 1]['flag'] == 0 and df.iloc[i]['flag'] == 1:
                buy_price = df.iloc[i]['close']
                k = k + 1
                # 初始化买入价格，历史最高价格，回撤比例
                if k == 1:
                    df.ix[i, 'money_cal'] = df.ix[i, 'close']
                    buy_price_init = df.ix[i, 'close']
                    max_price = buy_price_init
                    max_withdrawal_rate = 0
            if df.iloc[i - 1]['flag'] == 1 and df.iloc[i]['flag'] == 0:
                if buy_price is None:
                    continue
                else:
                    sell_price = df.iloc[i]['close']
                    return_rate = (sell_price - buy_price) / buy_price
                    if return_rate > 0:
                        o = o + 1
                        positive_return = return_rate + positive_return

                    if return_rate < 0:
                        p = p + 1
                        negative_return = return_rate + negative_return

                    df.ix[i, 'return_rate'] = return_rate
                    j = i
                    while pd.isnull(df.iloc[j]['money_cal']):
                        j = j - 1
                    df.ix[i, 'money_cal'] = df.ix[j, 'money_cal'] * return_rate + df.ix[j, 'money_cal']
                    # 取得当前价格之前的最高价格
                    if df.ix[i, 'money_cal'] > max_price:
                        max_price = df.ix[i, 'money_cal']
                    # 计算最大回撤比例
                    withdrawal_rate = 1 - (df.ix[i, 'money_cal'] / max_price)
                    # 比较所有的回撤比例，取得最大的回撤比例
                    if max_withdrawal_rate < withdrawal_rate:
                        max_withdrawal_rate = round(withdrawal_rate, 4)
                    # 计算策略年化收益率及资金曲线和股票本身年化收益率
                    times = round((df.ix[i, 'money_cal'] - buy_price_init) / buy_price_init / year_num, 2)
                    times_no_ma5 = round((df.ix[i, 'close'] - buy_price_init) / buy_price_init / year_num, 2)

    # 计算盈亏收益比
    if o == 0 or p == 0 or max_withdrawal_rate == 0:
        continue
    else:
        strategy_estimate = round(times / (max_withdrawal_rate * 100), 4)
        positive_return_average = positive_return / o
        negative_return_average = negative_return / p
        profit_to_loss_ratio = round(positive_return_average / abs(negative_return_average), 2)
        win_ratio = round(float(o) / float((o + p)), 2)
        df_ma_20_60_conclude.at[q, 'sz_code'] = stock_file[:9]
        df_ma_20_60_conclude.at[q, 'times'] = times
        df_ma_20_60_conclude.at[q, 'times_no_ma5'] = times_no_ma5
        df_ma_20_60_conclude.at[q, 'withdrawal'] = max_withdrawal_rate
        df_ma_20_60_conclude.at[q, 'strategy_estimate'] = strategy_estimate
        df_ma_20_60_conclude.at[q, 'profit_to_loss_ratio'] = profit_to_loss_ratio
        df_ma_20_60_conclude.at[q, 'win_ratio'] = win_ratio
    if times > times_no_ma5:
        m = m + 1
    else:
        n = n + 1
    pd.DataFrame.to_csv(df, target_dir + os.sep + stock_file, encoding='gbk')
pd.DataFrame.to_csv(df_ma_20_60_conclude, target_dir_conclude + os.sep + 'conclude.csv', encoding='gbk')
print (m, n)