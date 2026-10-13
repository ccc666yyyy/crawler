# import requests
# url="https://weibo.com/ajax/statuses/show?id=Rmenbnf29&locale=zh-CN&isGetLongText=true"
# header={
#     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36 Edg/155.0.0.0",
#     "Referer":"https://weibo.com/7200858608/Rmenbnf29"
# }
# res=requests.get(url,headers=header)
# res.encoding="utf-8"
# print(res.text)
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import json
from datetime import datetime
import csv
from urllib.parse import urlencode
import time

driver = webdriver.Edge()
url="https://weibo.com"
driver.get(url)

input("请在浏览器中完成登录，进入微博正文后按回车：")
sub_url="https://weibo.com/7200858608/Rmenbnf29"
driver.get(sub_url)
input("enter爬取一级评论：")
# result = driver.execute_async_script("""
#     const done = arguments[arguments.length - 1];
#
#     fetch("/ajax/statuses/show?id=Rmenbnf29&locale=zh-CN&isGetLongText=true")
#         .then(async response => ({
#             status: response.status,
#             body: await response.text()
#         }))
#         .then(done)
#         .catch(error => done({
#             error: String(error)
#         }));
# """)

# data = json.loads(result["body"])
# user=data["user"]["screen_name"]
# time=data["created_at"]
# time=datetime.strptime(time, "%a %b %d %H:%M:%S %z %Y")
# time=time.strftime("%Y-%m-%d %H:%M:%S")
# text=data["text_raw"]
# type="文字"
# reposts=data["reposts_count"]
# comments=data["comments_count"]
# attitudes=data["attitudes_count"]
# item=[user,time,text,type,reposts,comments,attitudes]

# with open("weibo_test.csv","a",encoding="utf-8",newline="") as f:
#     writer = csv.writer(f)
#     writer.writerow(["发布者","发布时间","微博内容","形式","转发数","评论数","点赞数"])
#     writer.writerow(item)
# 一级评论
all_comments = []
max_id = 0
for page in range(30):
    url = "/ajax/statuses/buildComments"

    params = {
        "is_reload": 1,
        "id": "5352984695539337",
        "is_show_bulletin": 2,
        "is_mix": 0,
        "count": 10,
        "uid": "7200858608",
        "fetch_level": 0,
        "locale": "zh-CN"
    }
    if page > 0:
        params["flow"] = 0
        params["max_id"] = max_id

    comment_url = url + "?" + urlencode(params)

    result1 = driver.execute_async_script("""
        const done = arguments[arguments.length - 1];

        fetch(arguments[0])
            .then(async response => ({
                status: response.status,
                body: await response.text()
            }))
            .then(done)
            .catch(error => done({
                error: String(error)
            }));
    """, comment_url)
    data = json.loads(result1["body"])

# print("一级评论数：", len(data["data"]))
# print("下一页游标：", data["max_id"])
    comment=data["data"]
    for item in comment:
        id=item["idstr"]
        user=item["user"]["screen_name"]
        created_at=item["created_at"]
        created_at=datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
        created_at=created_at.strftime("%Y-%m-%d %H:%M:%S")
        text=item["text_raw"]
        source = item.get("source", "")
        items=[id,user,text,created_at,source]
        all_comments.append(items)
    next_max_id = data["max_id"]

    if next_max_id == 0 or next_max_id == max_id:
        print("没有下一页，结束")
        break
    max_id = next_max_id
    time.sleep(2)
with open("weibo_comment1.csv","w",encoding="utf-8",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id","评论人","评论内容","评论时间","评论人ip"])
    writer.writerows(all_comments)

input("enter爬取二级评论：")

all_replies=[]
for comment in all_comments:
    parent_id=comment[0]
    count=0
    while True:
        reply_params = {
            "is_reload": 1,
            "id": parent_id,
            "is_show_bulletin": 2,
            "is_mix": 1,
            "fetch_level": 1,
            "max_id": 0,
            "count": 20,
            "uid": "7200858608",
            "locale": "zh-CN"
        }
        if count>0:
            reply_params["flow"] = 0
            reply_params["max_id"] = max_id

        url="/ajax/statuses/buildComments"
        reply_url = url + "?" + urlencode(reply_params)
        result2 = driver.execute_async_script("""
                const done = arguments[arguments.length - 1];

                fetch(arguments[0])
                    .then(async response => ({
                        status: response.status,
                        body: await response.text()
                    }))
                    .then(done)
                    .catch(error => done({
                        error: String(error)
                    }));
            """, reply_url)
        data = json.loads(result2["body"])
        for item in data["data"]:
            reply_id = item["idstr"]
            user = item["user"]["screen_name"]
            text = item["text_raw"]
            created_at = item["created_at"]
            created_at = datetime.strptime(created_at, "%a %b %d %H:%M:%S %z %Y")
            created_at = created_at.strftime("%Y-%m-%d %H:%M:%S")
            source = item.get("source", "")
            items = [reply_id,parent_id,user,text,created_at,source]
            all_replies.append(items)
        next_max_id = data["max_id"]
        if next_max_id == 0 or next_max_id == max_id:
            print("没有下一页，结束")
            break
        max_id = next_max_id
        time.sleep(2)
        count+=1
    with open("weibo_comment2.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["id","父id","评论人", "评论内容", "评论时间", "评论人ip"])
        writer.writerows(all_replies)




input("enter结束：")
driver.quit()