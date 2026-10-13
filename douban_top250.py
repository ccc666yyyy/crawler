import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

options=webdriver.EdgeOptions()
options.add_experimental_option("detach",True)
driver=webdriver.Edge(options=options)
sub_url=[]

for start in range(0,250,25):
    url="https://movie.douban.com/top250?start="+str(start)
    driver.get(url)

    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located(
            (By.XPATH, '//div[@class="hd"]/a')
        )
    )

    html = etree.HTML(driver.page_source)
    urls = html.xpath('//div[@class="hd"]/a/@href')

    sub_url.extend(urls)



with open('douban_top250.csv','a',encoding='utf-8',newline='') as f:
    writer=csv.writer(f)
    writer.writerow([
        "排名", "电影名称", "年份", "导演", "编剧", "主演",
        "类型", "国家", "语言", "上映日期", "片长",
        "又名", "评分", "评价人数", "星级占比", "剧情简介"
    ])

    for it in sub_url:
        driver.get(it)
        WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="content"]/h1/span[1]')
            )
        )

        sub_html=etree.HTML(driver.page_source)
        num=sub_html.xpath('//*[@id="content"]/div[1]/span[1]/text()')
        title=sub_html.xpath('//*[@id="content"]/h1/span[1]/text()')
        year=sub_html.xpath('//*[@id="content"]/h1/span[2]/text()')
        direct=sub_html.xpath('//*[@id="info"]/span[1]/span[2]/a/text()')
        if len(direct) > 1:
            direct = "/".join(direct)
        elif len(direct) == 1:
            direct = direct[0]

        dramatist=sub_html.xpath('//span[text()="编剧"]/following-sibling::span//a[not(@class="more-attrs")]/text()')

        if len(dramatist) > 1:
            dramatist = "/".join(dramatist)
        elif len(dramatist) == 1:
            dramatist = dramatist[0]

        actors=sub_html.xpath('//a[@rel="v:starring"]/text()')
        actors="/".join(actors)

        genre=sub_html.xpath('//span[@property="v:genre"]/text()')
        genre="/".join(genre)

        nation=sub_html.xpath('//span[text()="制片国家/地区:"]/following-sibling::text()[1]')
        language=sub_html.xpath('//span[text()="语言:"]/following-sibling::text()[1]')
        data=sub_html.xpath('//span[@property="v:initialReleaseDate"]/text()')
        data="/".join(data)
        runtime=sub_html.xpath('//span[@property="v:runtime"]/text()')
        another_name=sub_html.xpath('//span[text()="又名:"]/following-sibling::text()[1]')

        rate=sub_html.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/strong/text()')
        rate_num=sub_html.xpath('//*[@id="interest_sectl"]/div[1]/div[2]/div/div[2]/a/span/text()')
        star_rating=sub_html.xpath('//div[@class="ratings-on-weight"]//span[@class="rating_per"]/text()')
        star_rating="/".join(star_rating)

        profile = sub_html.xpath('//span[@property="v:summary"]//text()')
        hidden = sub_html.xpath('//span[@class="all hidden"]//text()')
        if hidden:
            profile = hidden
        profile="\n".join(s.strip() for s in profile if s.strip())
        writer.writerow([
            num[0] if num else "",
            title[0] if title else "",
            year[0] if year else "",
            direct,
            dramatist,
            actors,
            genre,
            nation[0].strip() if nation else "",
            language[0].strip() if language else "",
            data,
            runtime[0] if runtime else "",
            another_name[0].strip() if another_name else "",
            rate[0] if rate else "",
            rate_num[0] if rate_num else "",
            star_rating,
            profile
        ])

