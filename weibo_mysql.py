import csv
import pymysql

db = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="weibo_crawler",
    charset="utf8mb4"
)

cursor = db.cursor()
sql="""
INSERT INTO weibo_posts(author, created_at, content, content_type,
 reposts_count, comments_count, likes_count)
VALUES(%s,%s,%s,%s,%s,%s,%s)
"""
with open('weibo_text.csv', 'r' , encoding='utf-8-sig',newline='') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(sql, row)
sql="""
INSERT INTO weibo_comments(comment_id,username,content, created_at, source)
VALUES(%s,%s,%s,%s,%s)"""
with open('weibo_comment1.csv', 'r' , encoding='utf-8-sig',newline='') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        cursor.execute(sql, row)
sql="""
INSERT INTO weibo_replies(reply_id,parent_id,username,content, created_at, source)
VALUES(%s,%s,%s,%s,%s,%s)
"""
seen_ids = set()
with open('weibo_comment2.csv', 'r' , encoding='utf-8-sig',newline='') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        reply_id = row[0]

        if reply_id in seen_ids:
            continue
        seen_ids.add(reply_id)
        cursor.execute(sql, row)

db.commit()
cursor.close()
db.close()
