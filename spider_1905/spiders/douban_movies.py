# -*- coding: utf-8 -*-
"""
@Time   : 2020/3/31 9:49
@Author : Haojun Gao (github.com/VincentGaoHJ)
@Email  : gaohj@Scishang.com hjgao@std.uestc.edu.cn
@Sketch :
"""

import scrapy
from spider_1905.items import Spider1905Item
import json


class DoubanMovieSpider(scrapy.Spider):
    name = 'spider_1905'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=0&limit=20']
    offset = 0

    def parse(self, response):
        item = Spider1905Item()
        content_list = json.loads(response.body.decode())
        if (content_list == []):
            return
        for content in content_list:
            item['title'] = content['title']
            item['url'] = content['url']
            yield item
        self.offset += 20
        url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=100%3A90&action=&start=' + str(
            self.offset) + '&limit=20'
        yield scrapy.Request(url=url, callback=self.parse)
