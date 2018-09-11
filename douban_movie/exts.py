# 连接数据库和爬虫
from sqlalchemy import create_engine


engine = create_engine('mysql+pymysql://tim:87654321@localhost:3306/douban')
conn = engine.connect()

a = conn.execute('select 1').scalar()
print(a)