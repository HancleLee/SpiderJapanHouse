#!/usr/bin/env python
# -*- coding:utf-8 -*-

from Config import kDomain
import CityList

def startSpideJapanHouse() :
    houseList = ["/mansion/chuko/tokyo/",
                 "/mansion/chuko/kanagawa/",
                 "/mansion/chuko/chiba/",
                 "/mansion/chuko/saitama/",
                 "/mansion/chuko/kyoto/",
                 "/mansion/chuko/nara/"]
    names = ["東京", "神奈川", "千葉", "埼玉", "大阪", "京都", "奈良"]
    # href="/mansion/chuko/tokyo/"
    # href = "/mansion/chuko/kanagawa/"
    # href = "/mansion/chuko/chiba/"
    # href = "/mansion/chuko/saitama/"
    # href = "/mansion/chuko/kyoto/"
    # href = "/mansion/chuko/nara/"

    list_num = len(houseList)
    i = 0
    while (i < list_num):
        url = kDomain + houseList[i] + "city/"
        print("---------------------------------------------")
        print("开始爬取 %s 的数据 \n" %names[i])
        CityList.spiderArea(url, names[i])
        print("finish 爬取 %s 的数据完成 \n" %names[i])
        i += 1

startSpideJapanHouse()
print("end!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")