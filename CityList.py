#!/usr/bin/env python
# -*- coding:utf-8 -*-

import Urls
import City
import SecondHandHouse
import requests
import FileHelper
from Config import kDomain, kUserAgent

def spiderCityList(start_url, city_name, area_name):
    # start_url = "https://www.athome.co.jp/mansion/chuko/tokyo/chiyoda-city/list/"

    session = requests.Session()
    session.headers = {
        'User-Agent': kUserAgent
    }
    session.get(kDomain)
    r = session.get(start_url)
    # encode_type = r.encoding  # 本网址为'ISO-8859-1'
    # 文件保存时的编码格式
    encode_type = "utf-8"
    r_text = r.text.encode(encode_type).decode('utf-8')

    # 爬取整个区域
    print("begin-开始爬取城市 %s %s 的区域链接" %(city_name, area_name))
    try:
        urls = Urls.getAllPageUrls(start_url)
        print("finish-爬取城市 %s %s 区域链接完成-%d" % (city_name, area_name, len(urls)))
        index = 0
        for url in urls:
            spiderCityDetail(url=url, index=index, encode_type=encode_type, city_name=city_name, area_name= area_name)
            index += 1

    except (IOError, ZeroDivisionError) as e:
        print("error-爬取城市 %s %s 区域链接失败" %(city_name, area_name))

    # resultDic = SecondHandHouse.spiderHouseDetail("https://www.athome.co.jp/mansion/1025839326/location/?DOWN=1&BKLISTID=001LPC&IS_TAB_VIEW=1#item-detail_tabContents")
    # FileHelper.saveDic(resultDic, "house"+str(1), 'utf-8')


def spiderCityDetail(url, index, encode_type, city_name, area_name):
    print("开始爬取城市详情-%d %s %s %s"%(index,url, city_name, area_name))
    try:
        resultDic = {}
        house = SecondHandHouse.spiderHouseDetail(url)
        resultDic["city_name"] = city_name
        resultDic["area_name"] = area_name
        resultDic["house"] = house
        FileHelper.saveDic(resultDic, city_name + "_" + area_name + str(index), encode_type)
        print("爬取城市详情成功-%d %s %s %s" % (index, url, city_name, area_name))
    except (IOError, ZeroDivisionError) as e:
        print("error: 爬取城市详情失败-%d %s %s %s" % (index, url, city_name, area_name))


def spiderArea(url, city_name):
    areas = City.spiderCityList(url)
    print("areas", len(areas), areas)
    for area in areas:
        area = eval(area)
        area_name = area["area_name"]
        area_url = area["area_url"]
        print(area_name , area_url)
        spiderCityList(start_url=area_url, city_name=city_name, area_name=area_name)

# spiderArea("https://www.athome.co.jp/mansion/chuko/tokyo/city/", '东京')
# spiderCityList("https://www.athome.co.jp/mansion/chuko/tokyo/chiyoda-city/list/", "东京")
# print("end!!!!!!!!!!!!!!!!!!!!!!!!")
