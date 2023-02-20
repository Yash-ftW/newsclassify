import sqlite3 as sql

con = sql.connect('database_scrapy.db')
cur = con.cursor()
drop = "DROP TABLE nepali_news"
cur.execute(drop)
con.close()