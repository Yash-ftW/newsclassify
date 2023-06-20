import sqlite3 as sql

con = sql.connect('database_scrapy.db')
cur = con.cursor()

## To delete database content
try:
    drop = "DROP TABLE nepali_news"
    cur.execute(drop)
except:
    print("No Nepali Table")

try:
    drop = "DROP TABLE english_news"
    cur.execute(drop)
except:
    print("No English Table")

con.close()