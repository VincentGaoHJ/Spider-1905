# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json

import openpyxl


class Spider1905Pipeline(object):
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.sheet = self.wb.create_sheet("电影信息表")
        self.sheet.append(
            ["movie_id", "name", "scenario", "make", "feature", "score",
             "country", "type_info", "foreign_name", "duration", "color",
             "dimension", "name_varify", "playdate"])

    def process_item(self, item, spider):
        line = [str(item["movie_id"]), str(item["name"]), str(item["scenario"]),
                str(item["make"]), str(item["feature"]), str(item["score"]),
                str(item["country"]), str(item["type_info"]), str(item["foreign_name"]),
                str(item["duration"]), str(item["color"]), str(item["dimension"]),
                str(item["name_varify"]), str(item["playdate"])]
        self.sheet.append(line)
        self.wb.save("movie.xlsx")
        return item
