# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

import re
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
    a = re.compile('(\t|\n|\r)')
    new_list = [i.strip() for i in list_item]
    new_list = [a.sub('', i) for i in new_list]
    new_list = [i for i in new_list if i != ""]
    return "||".join(new_list)


def prep(item, key):
    if key not in item:
        return ""
    elif not item[key]:
        return ""
    elif isinstance(item[key], str):
        return item[key]
    elif isinstance(item[key], list):
        return list2str(item[key])
    else:
        raise Exception("Output item is not str nor list.")


class Spider1905Pipeline(object):
    def __init__(self):
        store_file = os.path.dirname(__file__) + '/spiders/movie_info.csv'
        self.file = open(store_file, 'w', newline='')
        self.writer = csv.writer(self.file)
        self.writer.writerow([
            "movie_id", "name", "scenario",
            "make", "feature", "score",
            "country", "type_info", "foreign_name",
            "duration", "color", "dimension",
            "name_varify", "playdate",

            "director", "playwright", "actor",
            "producer", "photographer", "montage",
            "music", "art_director", "assistant_director",
            "acrobats",

            "movie_url", "url_video", "url_still",
            "url_news", "url_review", "url_performer",
            "url_award", "url_scenario", "url_feature",
            "url_make", "url_info",
        ])

    def process_item(self, item, spider):
        self.writer.writerow([
            prep(item, "movie_id"), prep(item, "name"), prep(item, "scenario"),
            prep(item, "make"), prep(item, "feature"), prep(item, "score"),
            prep(item, "country"), prep(item, "type_info"), prep(item, "foreign_name"),
            prep(item, "duration"), prep(item, "color"), prep(item, "dimension"),
            prep(item, "name_varify"), prep(item, "playdate"),

            prep(item, "director"), prep(item, "playwright"), prep(item, "actor"),
            prep(item, "producer"), prep(item, "photographer"), prep(item, "montage"),
            prep(item, "music"), prep(item, "art_director"), prep(item, "assistant_director"),
            prep(item, "acrobats"),

            prep(item, "movie_url"), prep(item, "url_video"), prep(item, "url_still"),
            prep(item, "url_news"), prep(item, "url_review"), prep(item, "url_performer"),
            prep(item, "url_award"), prep(item, "url_scenario"), prep(item, "url_feature"),
            prep(item, "url_make"), prep(item, "url_info")
        ])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file.close()
