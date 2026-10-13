import requests
from lxml import etree
import csv
from py_mini_racer import MiniRacer
import json

url="https://www.shanghairanking.cn/rankings/bcur/2024"
header={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36 Edg/155.0.0.0",
    "Referer":url
}
payload_url = "https://www.shanghairanking.cn/_nuxt/static/1789974610/rankings/bcur/2024/payload.js"

r = requests.get(payload_url, headers=header)
r.encoding = "utf-8"

ctx=MiniRacer()
ctx.eval("""
var capturedData = null;

function __NUXT_JSONP__(path, data) {
    capturedData = data;
}
""")
ctx.eval(r.text)
json_text = ctx.eval("JSON.stringify(capturedData)")
data = json.loads(json_text)
ctx.close()
universities = data["data"][0]["univData"]
data=[]
for univ in universities:
    rank=univ["ranking"]
    name_cn=univ["univNameCn"]
    name_en=univ["univNameEn"]
    province=univ["province"]
    score=univ["score"]
    level=univ["indData"].get("536","")
    item=[rank,name_cn,name_en,province,score,level]
    data.append(item)

# html=etree.HTML(res.text)
# tr=html.xpath("//tbody/tr")
# data=[]
# for it in tr:
#     rank=it.xpath("./td[1]/div/text()")
#     name_cn=it.xpath('.//span[@class="name-cn"]/text()')
#     name_en=it.xpath('.//span[@class="name-en"]/text()')
#     province=it.xpath('./td[3]/text()')
#     score=it.xpath('./td[5]/text()')
#     level=it.xpath('./td[6]/text()')
#
#     item= [
#         x[0].strip() if x else ""
#         for x in [rank, name_cn, name_en, province, score, level]
#     ]
#     data.append(item)
#
with open("edu_ranking.csv","w",encoding="utf-8",newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["排名", "学校名称", "英文名称", "省份", "评分", "办学层次"])
    writer.writerows(data)

