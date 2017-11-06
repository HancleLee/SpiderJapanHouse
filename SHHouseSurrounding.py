#!/usr/bin/env python
# -*- coding:utf-8 -*-
import bs4
import requests
from bs4 import BeautifulSoup
import FileHelper
import SoupHelper
from Config import kDomain, kUserAgent

# test
url_test = "https://www.athome.co.jp/mansion/6964410290/?DOWN=1&BKLISTID=001LPC&IS_TAB_VIEW=1#item-detail_tabContents"

def spiderHouseSurrounding(url):
    url = url.replace("/?","/location/?")
    # print("开始爬取周边信息-%s" %url)
    result = {}
    session = requests.Session()
    session.headers = {
        'User-Agent': kUserAgent
    }
    session.get(kDomain)
    r = session.get(url)
    encode_type = r.encoding  # 本网址为'ISO-8859-1'
    r_text = r.text.encode(encode_type).decode('utf-8')

    section_facility = SoupHelper.filterTag(r_text, "section", {"id":"detail-facility"})
    div_list = SoupHelper.filterTag(section_facility, "div", {"class":"item-list clr formatCols col-4 zoomList"})
    div_items = SoupHelper.filterTags(div_list, "div", {"class":"item"})
    list_store = []
    for item in div_items:
        dic_store = {}
        p_items = SoupHelper.filterTags(item, "p", {})
        store_name = SoupHelper.tagTextNoSpace(p_items[0])
        distance = SoupHelper.tagTextNoSpace(p_items[1])
        # print(type(store_name), store_name)
        if type(store_name) == str:
            dic_store["store_name"] = store_name
            dic_store["store_distance"] = distance
            list_store.append(dic_store)

    # print(type(list_store),div_items)
    # 附近推荐
    if len(list_store)>0:
        result["recommend_nearby"] = list_store

    div_map_view = SoupHelper.filterTag(r_text, "div", {"id":"detail-map_view"})
    div_map = SoupHelper.filterTag(div_map_view, "div",{"id":"MAP"})
    # 经纬度
    # print(type(div_map),div_map)
    if type(div_map)==bs4.element.Tag:
        lat = div_map["lat"]
        lon = div_map["lon"]
        dic_map = {}
        if len(lat) > 0 and len(lon) > 0:
            dic_map["lat"] = lat
            dic_map["lon"] = lon
        result["map"] = dic_map

    return result


def filterTagTextNoSpace(tag, tag_name, attrs):
    return SoupHelper.tagTextNoSpace(SoupHelper.filterTag(tag=tag, tag_name=tag_name, attrs=attrs))

# spiderHouseSurrounding(url_test)