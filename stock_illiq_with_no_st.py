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
import time
from datetime import datetime as dt
import datetime as d


target_dir_illiq = 'D:/Program Files/tdx/vipdoc/sz/sz_illiq_compare'
data = pd.read_csv(target_dir_illiq + os.sep + 'illiq.csv')
data1 = sc.get_nost_stock(data)
pd.DataFrame.to_csv(data1, target_dir_illiq + os.sep + 'test.csv', encoding='gbk')