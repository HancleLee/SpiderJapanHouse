#!/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
from bs4 import BeautifulSoup
import FileHelper
import SoupHelper
from Config import kDomain, kUserAgent

# test
url_test = "https://www.athome.co.jp//mansion/shinchiku/116280/?DOWN=1&BKLISTID=001LPC&sref=list_simple&site_cd=0"

def spiderHouseDetail(url):
    session = requests.Session()
    session.headers = {
        'User-Agent': kUserAgent
    }
    session.get(kDomain)
    r = session.get(url)
    encode_type = r.encoding  # 本网址为'ISO-8859-1'
    r_text = r.text.encode(encode_type).decode('utf-8')

    # print(soup.prettify())

    div_content=SoupHelper.filterTag(r_text, "div", {"class":"pageSectionHeader sectionHeader propertyPageHeader"})
    # print(div_content)

    div_section_box = SoupHelper.filterTag(div_content, "div", {"class":"sectionHeadText"})

    div_detail_box1 = SoupHelper.filterTag(div_section_box, "div", {"class":"detailBox"})
    div_detail_box2 = SoupHelper.filterTag(div_section_box, "div", {"class":"detailBox detailPhaseBox phaseType1"})
    # print(div_detail_box)

    # title
    div_title = SoupHelper.filterTag(div_content, "div", {"class":"title"})
    house_title = SoupHelper.tagTextNoSpace(div_title)
    # address
    div_address = SoupHelper.filterTag(div_detail_box1, "div", {"class":"address"})
    house_address = SoupHelper.tagTextNoSpace(div_address)
    # traffic
    div_traffic = SoupHelper.filterTag(div_detail_box1, "div", {"class": "text"})
    house_traffic = SoupHelper.tagTextNoSpace(div_traffic)
    # house type
    div_house_types = SoupHelper.filterTagByLists(div_detail_box2, [["div", {"class":"boxInner"}], ["dl", {"class":"defListStyle horizontal defListType2"}]])
    dd_house_type = SoupHelper.filterTags(div_house_types, "dd", {"class":"item"})[0]
    dd_house_area = SoupHelper.filterTags(div_house_types, "dd", {"class":"item"})[1]
    house_type = SoupHelper.tagTextNoSpace(dd_house_type)
    house_area = SoupHelper.tagTextNoSpace(dd_house_area)

    # print(div_house_types)
    print(house_title, " # ", house_address, " # ", house_traffic, " # ", house_type, " # ", house_area)

spiderHouseDetail(url=url_test)