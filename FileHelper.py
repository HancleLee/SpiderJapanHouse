#!/usr/bin/env python
# -*- coding:utf-8 -*-
import datetime
import os

def saveDic(dic, file_name, encode_type):
    if type(dic)==dict:
        try:
            dic_num = dic.__len__()
            file_path = str(createFile()) + "\\" + file_name + '.txt'
            file_path = file_path.replace("\\", "/")
            fp = open(file_path, "w+", encoding=encode_type)
            fp.write(str(dic))
            # if type(dic) == dict:
            #     fp.write('{')
            #     index = 0
            #     for key, val in dic.items():
            #         fp.write(key)
            #         fp.write(':')
            #         if type(val) == str:
            #             fp.write(val)
            #         elif type(val) == list:
            #             fp.write('[')
            #             lists_num = val.__len__()
            #             for j in range(0, lists_num):
            #                 item = val[j]
            #                 fp.write(item)
            #                 if j < lists_num - 1:
            #                     fp.write(",")
            #                     # fp.write("\n")
            #             fp.write(']')
            #         if index < dic_num - 1:
            #             fp.write(",")
            #             fp.write("\n")
            #         index += 1
            #
            # if type(dic) == dict:
            #     fp.write('}')
            fp.close()
            return True

        except (IOError, ZeroDivisionError) as e:
            print(e)
            return False
    else:
        return False


def saveLists(lists, file_name, encode_type):
    # print(lists.__len__())
    if type(lists)==list:
        try:
            # 保存到文件
            file_path = str(createFile()) + "\\" + file_name + '.txt'
            file_path = file_path.replace("\\", "/")
            fp = open(file_path , "w+", encoding=encode_type)
            fp.write('[')
            lists_num = lists.__len__()
            for i in range(1, lists_num):
                item = lists[i]
                fp.write(item)
                if i < lists_num - 1:
                    fp.write(",")
            fp.write(']')
            fp.close()
            return True
        except (IOError ,ZeroDivisionError) as e:
            print(e)
            return False

    else:
        return False


def createFile():
    date = datetime.datetime.now().strftime('%Y%m%d')
    path = os.getcwd() + "\\" + date
    path = path.replace("\\", "/")
    print(path)
    if os.path.exists(path):
        return path
    else:
        os.mkdir(path)
        return path

