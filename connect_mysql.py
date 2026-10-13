import csv
import pymysql

db = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="douban_top250",
    charset="utf8mb4"
)

cursor = db.cursor()
# print("MySQL连接成功")
sql = """
INSERT INTO movies (
    num, title, year, direct, dramatist, actors,
    genre, nation, language, release_date, runtime,
    another_name, rate, rate_num, star_rating, profile
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s, %s, %s)
"""
count=0
with open('douban_top250.csv', 'r' , encoding='utf-8-sig',newline='') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(sql, row)
        count+=1

db.commit()
print(f"成功导入 {count} 条电影数据")
cursor.close()
db.close()