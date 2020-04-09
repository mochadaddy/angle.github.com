# coding: utf-8
import tushare as ts
import datetime as dt
import time
import stock_class as sc
import pandas as pd
import os


# 取tushare的token并连接api
def get_tocken():
    token = ts.set_token('71a5947e1d01e9b5c5275f2de127101940acd4cdb44cc2aad9c7e7cd')
    pro = ts.pro_api(token)
    return pro


# 取系统上一日
def get_sys_date():
    today = dt.date.today()
    yestorday = today - dt.timedelta(days=0)
    formatted_yestorday = yestorday.strftime('%Y%m%d')
    formatted_yestorday_int = str(formatted_yestorday)
    return formatted_yestorday_int

#取20年前的一天
def get_15_years_day():
    today = dt.date.today()
    yesterday = today - dt.timedelta(days=5475)
    formatted_yesterday = int(yesterday.strftime('%Y%m%d'))
    return formatted_yesterday



#取上一交易日
def get_last_trade_day():
    pro = sc.get_tocken()
    sys_date = sc.get_sys_date()
    trade_days = pro.trade_cal(exchange='', start_date='19910101', end_date=sys_date)
    trade_day = trade_days[trade_days['is_open'] == 1]
    last_trade_day = trade_day.sort_values('cal_date', ascending=False).head(1)
    last_trade_day_value = last_trade_day.iloc[0]['cal_date']
    return last_trade_day_value

#判断是否为交易日
def get_is_trade_day(date):
    isbolean = 'No'
    pro = sc.get_tocken()
    sys_date = sc.get_sys_date()
    trade_days = pro.trade_cal(exchange='', start_date='19910101', end_date=sys_date)
    trade_day = trade_days[trade_days['is_open'] == 1]
    row_num_day = trade_day.shape[0]
    for i in range(0, row_num_day):
        if trade_day.iloc[i]['cal_date'] == date:
            isbolean = 'yes'
            return isbolean
        else:
            continue
    return isbolean


# 取深证股票
def get_sz_stock():
    pro = sc.get_tocken()
    for _ in range(3):
        try:
            stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
            stock_list_sz = stock_list.loc[stock_list['ts_code'].str.contains('SZ')]
        except:
            time.sleep(2)
    return stock_list_sz


# 取上海股票
def get_sh_stock():
    pro = sc.get_tocken()
    for _ in range(3):
        try:
            stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
            stock_list_sh = stock_list.loc[stock_list['ts_code'].str.contains('SH')]
        except:
            time.sleep(2)
    return stock_list_sh


# 取年化回报数据
def get_return_rate(rate):
    target_annual_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare_annual_return/nhsy.csv'
    stock_list = pd.read_csv(target_annual_dir, usecols=['ts_code', 'year_annual_return'])
    stock_list_return = stock_list[stock_list['year_annual_return'] > rate]
    return stock_list_return


# 取区间收益
def get_backward_returns(stock_file, start_date, end_date, window):
    read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/day_download'
    target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_return_rate_cal'
    df = pd.read_csv(read_dir + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'open', 'close', 'pct_chg',
                                                               'vol', 'amount', 'MA_5', 'MA_10', 'MA_250'])
    row_num = df.shape[0]
    df_new = pd.DataFrame()
    df_new_window = pd.DataFrame()
    for i in range(0, row_num):
        if str(df.iloc[i]['trade_date']) == start_date: #and str(df.iloc[i]['trade_date']) <= end_date:
           df_new = df_new.append(df[i: i+1])
           df_new_window = df_new_window.append(df[i+window:i+window+1])
        else:
           continue
    if df_new.empty:
        return None
    else:
        df_new_reindex = df_new.reset_index(drop=True)
        frame = [df_new, df_new_window]
        df_union = pd.concat(frame)
        df_union_reindex = df_union.reset_index(drop=True)
        df_new_reindex['return'+str(window)] = df_union_reindex['close'].shift(-1) / df_new_reindex['close'] - 1.0
        #print df_new_reindex
        return df_new_reindex

# 剔除st和*st股票
def get_nost_stock(df):
    pro = sc.get_tocken()
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    data = data.loc[data['ts_code'].str.contains('SZ')]
    stock_num = df.shape[0]
    stock_name_num = data.shape[0]
    index = []
    for i in range(0, stock_num):
        for j in range(0, stock_name_num):
            if data.iloc[j]['ts_code'] == df.iloc[i]['ts_code']:
                stock_name = data.iloc[j]['name']
                if 'ST' not in stock_name:
                    break
                else:
                    index.append(i)
                    break
    data_with_no_st = df.drop(index)
    data_with_no_st = data_with_no_st.reset_index(drop=True)
    return data_with_no_st

# 获取股票流通市值
def get_stock_cap(ts_code, trade_date):
    read_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/sz_capital'
    #szlistfile = os.listdir(read_dir)
    stock_file = trade_date + '.csv'
    data = pd.read_csv(read_dir + os.sep + stock_file, usecols=['ts_code', 'trade_date', 'turnover_rate',
                                                                'circ_mv'])
    row_num = data.shape[0]
    for i in range(0, row_num):
        if ts_code == data.iloc[i]['ts_code']:
            return data[i:i+1]





