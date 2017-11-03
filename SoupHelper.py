#!/usr/bin/env python
# -*- coding:utf-8 -*-
import bs4
from bs4 import BeautifulSoup

def filterTagByLists(tag, lists):
    if type(lists)==list:
        for item in lists:
            if type(item)==list:
                if len(item)>1:
                    tag_name = item[0]
                    attrs = item[1]
                    tag = filterTag(tag, tag_name=tag_name, attrs=attrs)
    return tag



# 返回指定tag的数组
def filterTags(tag,tag_name, attrs):
    soup = BeautifulSoup(str(tag), 'lxml')
    result = soup.find_all(tag_name, attrs=attrs)
    return result

# 返回指定tag的第一个元素
def filterTag(tag,tag_name, attrs):
    soup = BeautifulSoup(str(tag), 'lxml')
    result = soup.find_all(tag_name, attrs=attrs)
    if result.__len__() > 0:
        return result[0]
    return False

# 返回tag中的文本并去除换行符和空格符
def tagTextNoSpace(tag):
    # print(type(tag))
    # print(tag.encoding)
    result = ""
    if type(tag)==bs4.element.Tag: # 标签
        result = tag.text.replace("\n", " ")
        result = result.replace(" ", "")
        result = result.replace("\t", "")
        result = result.replace("\xa0", " ")

    elif type(tag)==str:  # 文本
        result = tag.replace("\n", " ")
        result = result.replace(" ", "")
        result = result.replace("\t", "")
        result = result.replace("\xa0", " ")

    return result