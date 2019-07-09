# coding: utf-8
import tushare as ts
import datetime as dt
import stock_class as sc
import pandas as pd
import os


# 联接tushare的api接口
pro = sc.get_tocken()
# 得到系统日期的上一日
formatted_yestorday = sc.get_sys_date()
targetdir = 'D:/Program Files/tdx/vipdoc/cw/cwjx'
# 得到股票代码
stock_list = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# 得到交易最近的交易日期
df_trade_day = pro.trade_cal(exchange='', start_date='19910101', end_date=formatted_yestorday,
                             field='exchange, cal_date,is_open, pretrade_date')
df_trade_day_1 = df_trade_day[df_trade_day['is_open'] == 1]
df_trade_day_1_desc = df_trade_day_1.sort_values('cal_date', ascending=False)
df_trade_lastday = (df_trade_day_1_desc.iloc[0]['cal_date'])
# stock_list_sz = stock_list[stock_list['ts_code']]
df_capital = pro.daily_basic(ts_code='', trade_date=df_trade_lastday,
                             fields='ts_code,trade_date,total_share,float_share,total_mv,circ_mv')
stock_num = df_capital.shape[0]
stock_finanylize_capital = pd.DataFrame(index=range(0, stock_num), columns=['ts_code', 'trade_date',
                                                                                'float_share', 'total_mv',
                                                                                'circ_mv'])
# 筛选出深证股票列出市值
for i in range(0, stock_num):
    if df_capital.iloc[i]['ts_code'][7:9] == 'SZ':
        code = df_capital.ix[i, 'ts_code']
        trade_date = df_capital.ix[i, 'trade_date']
        float_share = df_capital.ix[i, 'float_share']
        total_mv = df_capital.ix[i, 'total_mv']
        circ_mv = df_capital.ix[i, 'circ_mv']
        stock_finanylize_capital.at[stock_finanylize_capital.index[i], 'ts_code'] = code
        stock_finanylize_capital.at[stock_finanylize_capital.index[i], 'trade_date'] = trade_date
        stock_finanylize_capital.at[stock_finanylize_capital.index[i], 'float_share'] = float_share
        stock_finanylize_capital.at[stock_finanylize_capital.index[i], 'total_mv'] = total_mv
        stock_finanylize_capital.at[stock_finanylize_capital.index[i], 'circ_mv'] = circ_mv
stock_finanylize_capital.to_csv(targetdir + os.sep + 'capital.csv', encoding='gbk')







