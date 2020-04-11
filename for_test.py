# coding: utf-8
import numpy as np

import pandas as pd
import os
import glob
import csv
import stock_class as sc
import numpy as np
import time
from datetime import datetime as dt
import datetime as d


pro = sc.get_tocken()
target_dir = 'D:/Program Files/tdx/vipdoc/sz/sz_tushare/sz_index'

df = pro.moneyflow_hsgt(start_date='20200201', end_date='20200410')
print(df)

