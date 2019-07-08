# coding=utf-8
import pandas as pd


# 导入数据 - 注意：这里请填写数据文件在您电脑中的路径
stock_data = pd.read_csv('D:/Program Files/tdx/vipdoc/sz/szlday/sz000001 .csv', parse_dates=[1])
# 将数据按照交易日期从远到近排序
stock_data.sort_values('date', inplace=True)
# ========== 计算移动平均线

# 分别计算5日、20日、60日的移动平均线
ma_list = [5, 20, 60]

# 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
for ma in ma_list:
    stock_data['MA_' + str(ma)] = stock_data['close'].rolling(window=ma, center=False).mean()

# 计算指数平滑移动平均线EMA
for ma in ma_list:
    # stock_data['EMA_' + str(ma)] = pd.ewma(stock_data['close'], span=ma)
    stock_data['EMA_' + str(ma)] = stock_data['close'].ewm(span=ma).mean()

# 将数据按照交易日期从近到远排序
stock_data.sort_values('date', ascending=False, inplace=True)

# ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
stock_data.to_csv('D:/Program Files/tdx/vipdoc/sz/sz_ma_calculate/sz000001_ma_ema.csv', index=False)
