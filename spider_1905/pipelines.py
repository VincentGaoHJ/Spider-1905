# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json


class Spider1905Pipeline(object):
    def open_spider(self, spider):
        self.file = open("douban.json", "w")
        self.num = 0

    def process_item(self, item, spider):
        self.num += 1
        content = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(content)
        return item

    def close_spider(self, spider):
        print('一共保存了' + str(self.num) + '条数据')
        self.file.close()
