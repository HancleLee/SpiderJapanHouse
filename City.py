#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
import SoupHelper
from Config import kDomain, kUserAgent

# 返回城市列表的数组， [{'area_name':'','area_url':'' }...] area_name:地区名 area_url:地区链接,数组里的object已经转换成str之后再存储的
def spiderCityList(url):
    if len(url)<=0:
        return ""
    area = {}
    results = []
    session = requests.Session()
    session.headers = {
        'User-Agent': kUserAgent
    }
    session.get(kDomain)
    r = session.get(url)
    encode_type = r.encoding  # 本网址为'ISO-8859-1'
    r_text = r.text.encode(encode_type).decode('utf-8')

    div_area_group = SoupHelper.filterTag(r_text, "div", {"class":"area-group search-items f-fixedTriggerCity"})
    sections = SoupHelper.filterTags(div_area_group, "section", {"class":"fieldgroup"})
    for item in sections:
        # print(item)
        ul_area = SoupHelper.filterTag(item, "ul", {"class":"typeInline col-5"})
        li_areas = SoupHelper.filterTags(ul_area, "li", {})
        for li in li_areas:
            # print(li)
            a_area = SoupHelper.filterTag(li, "a", {})
            if a_area:
                url = kDomain + a_area["href"]
                area_name = a_area.text
                area["area_name"] = area_name
                area["area_url"] = url
                # print(area)
                results.append(str(area))
    return results

# areas = spiderCityList("https://www.athome.co.jp/mansion/chuko/tokyo/city/")
# print(len(areas))
# print(areas)

# urls_1 = getUrlsFromCity("https://www.athome.co.jp/mansion/chuko/osaka/city/")
# print(len(urls_1))
# print(urls_1)