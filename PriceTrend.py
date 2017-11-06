#!/usr/bin/env python
# -*- coding:utf-8 -*-
import bs4
import requests
import SoupHelper
from Config import kDomain, kUserAgent
import re

# test
url_test = "https://www.athome.co.jp/mansion/chuko/souba/tokyo/chiyoda-city/"

def spiderPriceTrend(url):
    # print(url)
    session = requests.Session()
    session.headers = {
        'User-Agent': kUserAgent
    }
    session.get(kDomain)
    r = session.get(url)
    encode_type = r.encoding  # 本网址为'ISO-8859-1'
    r_text = r.text.encode(encode_type).decode('utf-8')

    script = SoupHelper.filterTags(r_text, "script", {})

    pattern = re.compile(r'chartData = .+')

    # 使用search()查找匹配的子串，不存在能匹配的子串时将返回None
    # 这个例子中使用match()无法成功匹配
    match = pattern.search(str(script))
    chartData = str(match.group())
    chartData = chartData.split("=")[1].split(";")[0]
    # print(chartData)
    try:
        chartData = eval(chartData)
    except (IOError) as e:
        print("PriceTrend str to dict fail")
    if len(chartData)>0:
        return chartData
    else:
        return False

# spiderPriceTrend(url_test)