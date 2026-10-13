import pymysql
import matplotlib.pyplot as plt

db = pymysql.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="root",
    database="weibo_crawler",
    charset="utf8mb4"
)

cursor = db.cursor()

sql = """
SELECT
    HOUR(created_at) AS hour,
    COUNT(*) AS comment_count
FROM (
    SELECT created_at FROM weibo_comments
    UNION ALL
    SELECT created_at FROM weibo_replies
) AS all_comments
GROUP BY HOUR(created_at)
ORDER BY hour
"""

cursor.execute(sql)
result = cursor.fetchall()

hours = [row[0] for row in result]
counts = [row[1] for row in result]

plt.bar(hours, counts)

plt.xlabel("Hour")
plt.ylabel("Comment Count")
plt.title("Weibo Comments by Hour")

plt.xticks(range(24))
plt.tight_layout()
plt.show()

cursor.close()
db.close()