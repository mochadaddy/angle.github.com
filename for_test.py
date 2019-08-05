# coding: utf-8
import pymysql as pm
# 连接数据库 并添加cursor游标

conn = pm.connect('127.0.0.1', 'root', 'rootroot', 'stock')
cursor = conn.cursor()
print cursor

sql_insert = "select * from stock.stock_test"
cursor.execute(sql_insert)
rows = cursor.fetchall()
for row in rows:
    print row



