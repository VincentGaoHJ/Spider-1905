# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

import os
import csv
import openpyxl


# class Spider1905Pipeline(object):
#     def __init__(self):
#         self.wb = openpyxl.Workbook()
#         self.sheet = self.wb.create_sheet("电影信息表")
#         self.sheet.append(
#             ["movie_id", "name", "scenario",
#              "make", "feature", "score",
#              "country", "type_info", "foreign_name",
#              "duration", "color", "dimension",
#              "name_varify", "playdate"])
#
#     def process_item(self, item, spider):
#         line = [str(item["movie_id"]), str(item["name"]), str(item["scenario"]),
#                 str(item["make"]), str(item["feature"]), str(item["score"]),
#                 str(item["country"]), str(item["type_info"]), str(item["foreign_name"]),
#                 str(item["duration"]), str(item["color"]), str(item["dimension"]),
#                 str(item["name_varify"]), str(item["playdate"])]
#         self.sheet.append(line)
#         self.wb.save("movie.xlsx")
#         return item
def list2str(list_item):
    new_list = [i for i in list_item if i != ""]
    new_list = [i.strip() for i in new_list]
    return "||".join(new_list)


def prep(single_item):
    if isinstance(single_item, str):  # 判断是否为字符串类型
        return single_item
    elif single_item is None:
        return ""
    elif isinstance(single_item, list):
        return list2str(single_item)
    else:
        raise Exception("Output item is not str nor list.")


class Spider1905Pipeline(object):
    def __init__(self):
        store_file = os.path.dirname(__file__) + '/spiders/movie_info.csv'
        self.file = open(store_file, 'w', newline='')
        self.writer = csv.writer(self.file)

    def process_item(self, item, spider):
        # 判断字段值不为空再写入文件
        print(prep(item["make"]))
        print(prep(item["feature"]))
        print(prep(item["score"]))
        self.writer.writerow([prep(item["movie_id"]), prep(item["name"]), prep(item["scenario"]),
                              prep(item["make"]), prep(item["feature"]), prep(item["score"]),
                              ])

        # self.writer.writerow([prep(item["movie_id"]), prep(item["name"]), prep(item["scenario"]),
        #                       prep(item["make"]), prep(item["feature"]), prep(item["score"]),
        #                       prep(item["country"]), prep(item["type_info"]), prep(item["foreign_name"]),
        #                       prep(item["duration"]), prep(item["color"]), prep(item["dimension"]),
        #                       prep(item["name_varify"]), prep(item["playdate"])])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()
