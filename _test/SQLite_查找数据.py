import sqlite3

conn = sqlite3.connect('deals.db')
c = conn.cursor()

sql = 'SELECT * FROM deals WHERE ASIN = "B09XWP2XZQ"'
c.execute(sql)
results = c.fetchall()
print(results)
# [('link1', 'B09XWP2XZQ', ...), 
#  ('link2', 'B09XWP2XZQ', ...)]

# 或者只查询部分字段
sql = 'SELECT Link, ASIN, Title FROM deals WHERE ASIN = "B09XWP2XZQ"'
c.execute(sql)
results = c.fetchall()
print(results)
#[('link1', 'B09XWP2XZQ', 'title1'), 
# ('link2', 'B09XWP2XZQ', 'title2')]

conn.close()