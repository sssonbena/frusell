import os
try:
    os.unlink('fruit.db')
except:
    print('首次建檔')

import sqlite3

dbname = 'fruit.db'
if os.path.exists(dbname):
    os.unlink(dbname)
# 新建並連接資料庫 (Create and Connect a Database)
conn = sqlite3.connect(dbname)
cur = conn.cursor()
# 新建並連接資料庫 
conn = sqlite3.connect(dbname)
cur = conn.cursor()

# 水果表
cur.execute('''CREATE TABLE FRUIT
    (FRUIT_CODE text, FRUIT_NAME text, PRICE_PACK integer, PRICE_BOX integer)''')
# 水果表初始資料
cur.execute("INSERT INTO FRUIT VALUES ('1001','青森蘋果',60,350)")
cur.execute("INSERT INTO FRUIT VALUES ('1002','富士蘋果',55,320)")
cur.execute("INSERT INTO FRUIT VALUES ('2001','寶島蕉',20,200)")
cur.execute("INSERT INTO FRUIT VALUES ('2002','美人蕉',15,150)")
cur.execute("INSERT INTO FRUIT VALUES ('3011','大湖草莓(小)',0,100)")
cur.execute("INSERT INTO FRUIT VALUES ('3012','大湖草莓(中)',0,150)")
cur.execute("INSERT INTO FRUIT VALUES ('3013','大湖草莓(大)',0,200)")
cur.execute("INSERT INTO FRUIT VALUES ('3020','日本草莓',40,300)")
conn.commit()
# 查詢水果表
cur.execute("SELECT * FROM FRUIT")
fruit = cur.fetchall()
for row in fruit:
    print(row)

#商店據點表
cur.execute('''CREATE TABLE STORE
    (STORE_ID text, STORE_NAME text, STORE_ADDRESS text, STORE_TEL text, BUSINESS_HOURS text)''')
#商店據點初始資料
cur.execute("INSERT INTO STORE VALUES ('01','水果小舖','807高雄市超級區無敵路66號','(07)123-6666','9:00-22:00')")
# 查詢商店據點表
cur.execute("SELECT * FROM STORE")
members = cur.fetchall()
for row in members:
    print(row)

# 會員表
cur.execute('''CREATE TABLE MEMBERS
    (MEMBER_ID text,MEMBER_NAME text,GENDER text,BIRTH_YEAR integer)''')
# 會員表初始資料
cur.execute("INSERT INTO MEMBERS VALUES ('A01','Bug','M',1987)")
cur.execute("INSERT INTO MEMBERS VALUES ('A02','Ian','M',1952)")
cur.execute("INSERT INTO MEMBERS VALUES ('A03','Amy','F',1997)")
conn.commit()
# 查詢會員表
cur.execute("SELECT * FROM MEMBERS")
members = cur.fetchall()
for row in members:
    print(row)

# 銷售表
cur.execute('''CREATE TABLE SALES
    (SDATE text,MEMBER_ID text,FOLIO integer,FRUIT_CODE text,PACK_NUM integer,PRICE_PACK integer,
    BOX_NUM integer,PRICE_BOX integer,AMOUNT integer)''')
conn.commit()
# 查詢銷售表
cur.execute("SELECT * FROM SALES")
sales = cur.fetchall()
for row in sales:
    print(row)


# 關閉資料庫連接 (Close the Connection)
conn.close()

