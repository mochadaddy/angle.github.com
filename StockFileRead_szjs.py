# coding=utf-8
import csv
import pandas as pd
import os


filename = raw_input("请输入以cwjx开头+YYYYMMDD格式日期的财务数据文件名称：")
# filename_date = filename[4:12]
# filename = 'cwjx20130930'
filename_date = filename[4:12]
# 财务数据文件读取
d2 = pd.read_csv('D:/Program Files/tdx/vipdoc/cw/cwjx/' + filename + '.csv', usecols=['StockCode', '238_zgb'])
# 财务数据条数
d2_record_num = (int(d2.describe().ix[0, 0]))
# csv转换成dataframe
stock_finanylize_capital = pd.DataFrame(index=range(0, d2_record_num), columns=['stock_code', 'stock_date',
                                                                                'stock_sum_capitalization'])

# 定义输出文件位置
targetdir= 'D:/Program Files/tdx/vipdoc/cw/cwjx'

# 遍历日线数据文件
for info in os.listdir('D:/Program Files/tdx/vipdoc/sz/szlday/'):
    path = os.path.abspath(r'D:/Program Files/tdx/vipdoc/sz/szlday/')
    full_file_name = os.path.join(path, info)
    #print full_file_name

    # 日线数据文件读取
    d1 = pd.read_csv(full_file_name, usecols=['code', 'date', 'close'])
    # 日线数据文件条数
    d1_record_num = (int(d1.describe().ix[0, 0]))
    # 按照日期降序排列
    d1_select_by_date = (d1.loc[d1['date'].isin([filename_date])])
    first_row = pd.DataFrame(d1_select_by_date.reset_index(drop=True))
    #print first_row
    #print(int(d1_select_by_date.iloc['code']))

    #d1_sortbydesc = d1.sort_values(by='date', ascending=False)
    # 读取第一条记录
    # first_row = d1_sortbydesc.head(1)
    # 读取每个字段的值并转换成int
    if (int(first_row.describe().ix[0, 0])) == 1:
        stock_code = int(first_row.iloc[0]['code'])
        stock_date = int(first_row.iloc[0]['date'])
        stock_price = first_row.iloc[0]['close']
        #print stock_code

    # 遍历财务数据与日线数据的code值做匹配，当code相同时，得到该股票市值
        for j in range(0, d2_record_num):
            stock_code_finanylize = d2.ix[j, 'StockCode']
            stock_capital_finanylize = d2.ix[j, '238_zgb']
            if stock_code == stock_code_finanylize:
                stock_sum_capitalization = stock_price * stock_capital_finanylize
            # 转换成csv前的赋值
                stock_finanylize_capital.at[stock_finanylize_capital.index[j], 'stock_code'] = stock_code
                stock_finanylize_capital.at[stock_finanylize_capital.index[j], 'stock_date'] = stock_date
                stock_finanylize_capital.at[stock_finanylize_capital.index[j],
                                        'stock_sum_capitalization'] = stock_sum_capitalization
# 输出csv文件
stock_finanylize_capital.to_csv(targetdir + os.sep + 'capital.csv', encoding='gbk')

