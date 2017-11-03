#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Urls
import City
import SecondHandHouse
import requests
import FileHelper
from Config import kDomain, kUserAgent

start_url = "https://www.athome.co.jp/mansion/chuko/tokyo/chiyoda-city/list/"

session = requests.Session()
session.headers = {
    'User-Agent': kUserAgent
}
session.get(kDomain)
r = session.get(start_url)
encode_type = r.encoding  # 本网址为'ISO-8859-1'
r_text = r.text.encode(encode_type).decode('utf-8')

# 爬取整个区域
# urls = Urls.getAllPageUrls(start_url)
# print(len(urls))
# index = 0
# for url in urls:
#     print(url)
#     resultDic = SecondHandHouse.spiderHouseDetail(url)
#     FileHelper.saveDic(resultDic, "house"+str(index), encode_type)
#     index += 1

resultDic = SecondHandHouse.spiderHouseDetail("https://www.athome.co.jp/mansion/1025839326/location/?DOWN=1&BKLISTID=001LPC&IS_TAB_VIEW=1#item-detail_tabContents")
FileHelper.saveDic(resultDic, "house"+str(1), 'utf-8')

print("end!!!!!!!!!!!!!!!!!!!!!!!!")
