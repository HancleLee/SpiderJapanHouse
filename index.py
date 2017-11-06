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


# 'city_name': 城市名, 'area_name': 区域, 'house':房屋数据 {
# 'home_link_id': 链接，
# 'build_price': 价格,
# 'build_floor': 楼层,
# 'build_traffic': '交通',
# 'address': 地址,
# 'build_time': 施工日期,
# 'build_sqr': 建筑面积,
# 'build_type': 房屋类型,
# 'price_trend_url': 区域价格趋势对应的链接,
#  'price_trend_chart_data': 区域价格趋势对应的数据,
# 'management_cost': 管理费,
#  'reserve_fund': 储蓄金,
#  'build_name': 房屋名,
#  'note': 备注,
#  'orientation': 朝向,
# 'status': 状态,
#  'creat_time': 上线日期 ，
# 'pics': 房屋照片，以"；"分割,
#  'surround': 房屋周边环境，{'recommend_nearby':附近推荐 [{'store_name': '附近推荐名称', 'store_distance': '附近推荐距离'}], 'map': {经纬度}}}}