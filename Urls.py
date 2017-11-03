#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from Config import kDomain, kUserAgent
import SoupHelper

# 返回本页所有urls数组
def getListUrls(url):
    if len(url)<=0:
        return []
    session = requests.Session()
    session.headers = {
        'User-Agent': kUserAgent
    }
    session.get(kDomain)
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'lxml')

    all_div = soup.select('div[data-event^="clicktracking"]')
    lits_url = []
    # 循环div获取详细信息
    for item in all_div:
        p_title = SoupHelper.filterTag(item, 'p', {'class': 'heading object-title'})
        title = SoupHelper.tagTextNoSpace(p_title.a)
        a_href = p_title.a["href"]
        detail_url = kDomain + str(a_href)
        lits_url.append(detail_url)

    return lits_url

# 返回下一页
def getNextPage(url):
    if len(url)<=0:
        return ""

    session = requests.Session()
    session.headers = {
        'User-Agent': kUserAgent
    }
    session.get(kDomain)
    r = session.get(url)
    encode_type = r.encoding  # 本网址为'ISO-8859-1'
    r_text = r.text.encode(encode_type).decode('utf-8')

    next_url = ""
    div_footer = SoupHelper.filterTag(r_text, "div", {"class": "list-footer separater"})
    div_page = SoupHelper.filterTag(div_footer, "div", {"class": "line clr"})
    ul_page = SoupHelper.filterTag(div_page, "ul", {"class": "paging typeInline"})
    li_pages = SoupHelper.filterTags(ul_page, "li", {})
    li_num = len(li_pages)
    if li_num>0:
        li_last = li_pages[li_num - 1]
        a_li_last = SoupHelper.filterTags(li_last, "a", {})
        if len(a_li_last) > 1:
            a_last = a_li_last[0]
            next_url = kDomain + a_last["href"]
    return next_url

# 返回所有页面的urls数组
def getAllPageUrls(start_url):
    urls = getListUrls(start_url)
    next_url = getNextPage(start_url)
    all_urls = urls
    while True:
        urls = getListUrls(next_url)
        for item in urls:
            all_urls.append(item)

        if len(next_url) <= 0:
            break
        next_url = getNextPage(next_url)

    return all_urls

