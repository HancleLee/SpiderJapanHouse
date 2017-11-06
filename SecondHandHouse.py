#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re

import bs4
import requests
from bs4 import BeautifulSoup
import FileHelper
import PriceTrend
import SoupHelper
from Config import kDomain, kUserAgent
import SHHouseSurrounding

# test
url_test = "https://www.athome.co.jp/mansion/6964410290/?DOWN=1&BKLISTID=001LPC&IS_TAB_VIEW=1#item-detail_tabContents"

def spiderHouseDetail(url):
    result = {}
    result["home_link_id"] = url

    session = requests.Session()
    session.headers = {
        'User-Agent': kUserAgent
    }
    session.get(kDomain)
    r = session.get(url)
    encode_type = r.encoding  # 本网址为'ISO-8859-1'
    r_text = r.text.encode(encode_type).decode('utf-8')

    div_basic_right = SoupHelper.filterTagByLists(r_text, [["div", {"id":"item-detai_basic"}], ["div", {"class":"right"}]])
    dl_table = SoupHelper.filterTags(div_basic_right,"dl", {"class":"data typeTable"})
    if len(dl_table) >= 4:
        dl_0 = dl_table[0]
        dl_1 = dl_table[1]
        dl_2 = dl_table[2]
        dl_3 = dl_table[3]
        dd_price = filterTagTextNoSpace(dl_0,"dd", {"class":"cell02"}) # 价格
        dd_floor = filterTagTextNoSpace(dl_0,"dd", {"class":"cell04"}) # 楼层
        dd_traffic = filterTagTextNoSpace(dl_1, "dd", {}) # 交通
        dd_address = filterTagTextNoSpace(dl_2, "dd", {}) # 地址
        result["build_price"] = dd_price
        result["build_floor"] = dd_floor
        result["build_traffic"] = dd_traffic
        result["address"] = dd_address

        dd_3_arr = SoupHelper.filterTags(dl_3, "dd",{})
        if len(dd_3_arr) >= 3 :
            dd_build_creat_time = SoupHelper.tagTextNoSpace(dd_3_arr[0]) # 施工日期
            dd_area_cover = SoupHelper.tagTextNoSpace(dd_3_arr[1]) # 建筑面积
            dd_house_type = SoupHelper.tagTextNoSpace(dd_3_arr[2]) # 房子类型
            result["build_time"] = dd_build_creat_time
            result["build_sqr"] = dd_area_cover
            result["build_type"] = dd_house_type

    div_item_detail = SoupHelper.filterTagByLists( r_text,[["section",{"id": "item-detail_data"}], ["div",{"class":"clr"}], ["div",{"class":"left"}]])
    table_items = SoupHelper.filterTags(div_item_detail, "table",{})
    if len(table_items)>=3:
        table_detail_0 = table_items[0]
        tr_details_0 = SoupHelper.filterTags(table_detail_0, "tr", {})
        if len(tr_details_0) >= 4:
            tr_detail_0_2 = tr_details_0[2]
            tr_detail_a_0 = SoupHelper.filterTag(tr_detail_0_2, "a", {})
            if type(tr_detail_a_0)==bs4.element.Tag:
                tr_detail_a_href = tr_detail_a_0["href"]
                if len(tr_detail_a_href) > 0:
                    price_trend = kDomain + tr_detail_a_href  # 城市报价链接
                    result["price_trend_url"] = price_trend
                    chartData = getPriceTrendDetail(price_trend)
                    result["price_trend_chart_data"] = chartData

        table_detail_1 = table_items[1]
        tr_details = SoupHelper.filterTags(table_detail_1, "tr",{})
        if len(tr_details)>=4:
            tr_detail_1 = tr_details[1]
            td_details  = SoupHelper.filterTags(tr_detail_1, "td", {})
            td_manager_price = SoupHelper.tagTextNoSpace(td_details[0]) # 管理费
            td_store_price = SoupHelper.tagTextNoSpace(td_details[1])   # 储存金
            result["management_cost"] = td_manager_price
            result["reserve_fund"] = td_store_price

        table_detail_2 = table_items[2]
        tr_details_2 = SoupHelper.filterTags(table_detail_2, "tr", {})
        if len(tr_details_2) >= 4:
            tr_detail_2_0 = tr_details_2[0]
            td_details_2_0 = SoupHelper.filterTags(tr_detail_2_0, "td", {})
            td_build_name = SoupHelper.tagTextNoSpace(td_details_2_0[0])  # 建筑名
            result["build_name"] = td_build_name

            tr_detail_2 = tr_details_2[3]
            td_details_2 = SoupHelper.filterTags(tr_detail_2, "td", {})
            td_note = SoupHelper.tagTextNoSpace(td_details_2[0]) # 备注
            result["note"] = td_note

            try:
                pattern = re.compile(r'採光面：.+')
                # 使用search()查找匹配的子串，不存在能匹配的子串时将返回None
                # 这个例子中使用match()无法成功匹配
                td_note_str = SoupHelper.tagText(td_details_2[0])
                match = pattern.search(str(td_note_str))
                print(type(match))
                if match != None:
                    orientation = str(match.group())
                    if len(orientation) > 0:
                        orientation = orientation.replace("採光面：", "")
                    if len(orientation) > 0:
                        result["orientation"] = orientation  # 朝向
                        # print(orientation)
            except (IOError) as e:
                print("SecondHandHouse line101 get orientation failed")


        table_detail_4 = table_items[4]
        tr_details_4 = SoupHelper.filterTags(table_detail_4, "tr", {})
        if len(tr_details_4) >= 3:
            tr_detail_4_0 = tr_details_4[0]
            td_details_4_0 = SoupHelper.filterTags(tr_detail_4_0, "td", {})
            td_status = SoupHelper.tagTextNoSpace(td_details_4_0[1])  # 现状
            result["status"] = td_status

            tr_detail_4 = tr_details_4[2]
            td_details_4 = SoupHelper.filterTags(tr_detail_4, "td", {})
            td_build_post_time = SoupHelper.tagTextNoSpace(td_details_4[0])  # 上线日期
            result["creat_time"] = td_build_post_time

    ul_imglist = SoupHelper.filterTag(r_text, 'ul', {"class":"image-list horizontal clr zoomList"})
    li_imgs = SoupHelper.filterTags(ul_imglist, "li",{"class":"item"})
    a_src = ""
    for li in li_imgs:
        img_img = SoupHelper.filterTag(li, "img", {})
        a_src = a_src + img_img["src"] # 房屋照片，以；分割
        a_src = a_src + "; "

    result["pics"] = a_src
    try:
        dic_surround = SHHouseSurrounding.spiderHouseSurrounding(url=url)
        if len(dic_surround) > 0:
            result["surround"] = dic_surround
    except (IOError, ZeroDivisionError) as e:
        print("爬取周边信息失败 %s" %url)

    return result


def filterTagTextNoSpace(tag, tag_name, attrs):
    return SoupHelper.tagTextNoSpace(SoupHelper.filterTag(tag=tag, tag_name=tag_name, attrs=attrs))

def getPriceTrendDetail(url):
    return PriceTrend.spiderPriceTrend(url)

# spiderHouseDetail(url=url_test)

