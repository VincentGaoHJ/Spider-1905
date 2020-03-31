# -*- coding: utf-8 -*-
"""
@Time   : 2020/3/31 9:49
@Author : Haojun Gao (github.com/VincentGaoHJ)
@Email  : gaohj@Scishang.com hjgao@std.uestc.edu.cn
@Sketch :
"""

import itertools
import scrapy

from scrapy import Request
from spider_1905.items import Spider1905Item


class DoubanMovieSpider(scrapy.Spider):
    name = 'spider_1905'
    allowed_domains = ['1905.com']

    def start_requests(self):
        country_list = ["India"]
        year_list = list(range(2014, 2021))
        for country_info, year_info in itertools.product(country_list, year_list):
            url = f"https://www.1905.com/mdb/film/list/country-{str(country_info)}/year-{str(year_info)}"
            info_complete = f"{country_info}{year_info}"
            yield Request(url=url, callback=getattr(self, info_complete + '_parse', self.parse))

    def parse(self, response):
        # 整个一年的影片数量
        # movie_number = response.xpath('//div[contains(@class,"lineG")]/text()').extract_first()

        movie_list = response.xpath('//ul[contains(@class,"inqList")]/li')
        for movie_contend in movie_list:
            item = Spider1905Item()

            name = movie_contend.xpath('div/p/a/@title').extract()
            href = movie_contend.xpath('div/p/a/@href').extract_first()

            movie_id = href.split("/")[-2]
            url = "https://www.1905.com" + href

            item["name"] = name
            item["movie_id"] = movie_id
            item["movie_url"] = url

            yield Request(url=url, meta={'item': item},
                          callback=self.parse_movie_main)

        next_page = response.xpath('//div[@id="new_page"]/a[contains(text(),"下一页")]/@href').extract_first()
        if next_page:
            next_page = "https://www.1905.com" + next_page
            print(f"Starting process website: {next_page}")
            yield scrapy.Request(url=next_page, callback=self.parse)
        else:
            print("Congratulations!!!!")

    def parse_movie_main(self, response):

        item = response.meta['item']

        navigation = response.xpath('//nav[@class="navigation"]/ul/li')
        navigation_more = response.xpath('//nav[@class="navigation"]/div/ul/li')

        navi_dict = {}
        for navi_item in navigation:
            navi_key = navi_item.xpath("a/text()").extract_first()
            navi_href = navi_item.xpath("a/@href").extract_first()
            navi_dict[navi_key] = navi_href
        for navi_item in navigation_more:
            navi_key = navi_item.xpath("a/text()").extract_first()
            navi_href = navi_item.xpath("a/@href").extract_first()
            navi_dict[navi_key] = navi_href

        key_pair = [("在线观看", "url_video"),
                    ("图片", "url_still"),
                    ("新闻", "url_news"),
                    ("影评", "url_review"),
                    ("演职人员", "url_performer"),
                    ("获奖信息", "url_award"),
                    ("更多资料", "url_scenario")]

        for info_key, info_eng in key_pair:
            if info_key in navi_dict:
                if navi_dict[info_key]:
                    url = "https://www.1905.com" + navi_dict[info_key]
                    item[info_eng] = url
                else:
                    item[info_eng] = None
            else:
                item[info_eng] = None

        yield Request(url=item["url_scenario"], meta={'item': item},
                      callback=self.parse_movie_scenario)

    def parse_movie_scenario(self, response):

        item = response.meta['item']

        scenario = response.xpath('//li[@class="more-infos-plot showInfos"]/p/text()').extract_first()
        item["scenario"] = scenario
        more_infos = response.xpath('//div[@class="more-info-list"]/a')
        more_info_dict = {}
        for more_info in more_infos:
            more_info_key = more_info.xpath("text()").extract_first()
            more_info_href = more_info.xpath("@href").extract_first()
            more_info_dict[more_info_key] = more_info_href

        key_pair = [("幕后花絮", "url_feature"),
                    ("机构信息", "url_make"),
                    ("详细信息", "url_info")]
        for info_key, info_eng in key_pair:
            if info_key in more_info_dict:
                if more_info_dict[info_key]:
                    url = "https://www.1905.com" + more_info_dict[info_key]
                    item[info_eng] = url
                else:
                    item[info_eng] = None
            else:
                item[info_eng] = None

        if item["url_feature"]:
            yield Request(url=item["url_feature"], meta={'item': item},
                          callback=self.parse_movie_feature)

    def parse_movie_feature(self, response):

        item = response.meta['item']

        feature = response.xpath('//dd/text()').extract()
        item["feature"] = feature

        if item["url_make"]:
            yield Request(url=item["url_make"], meta={'item': item},
                          callback=self.parse_movie_make)

    def parse_movie_make(self, response):
        item = response.meta['item']

        make = response.xpath('//dd[@class="icon_all"]/text()').extract()
        item["make"] = make

        if item["url_info"]:
            yield Request(url=item["url_info"], meta={'item': item},
                          callback=self.parse_movie_info)

    def parse_movie_info(self, response):
        item = response.meta['item']

        infos_1 = response.xpath('//ul[contains(@class,"clearfloat")]')
        info_dict = {}
        for info in infos_1:
            info_key_list = info.xpath('dl/dt/text()').extract()
            info_value_list = info.xpath('dl/dd/text()').extract()
            for i in range(len(info_key_list)):
                info_key = "".join(info_key_list[i].split())
                info_value = info_value_list[i].split()
                info_dict[info_key] = info_value

        infos_2 = response.xpath('//dl[contains(@class,"clearfloat")]')
        for info in infos_2:
            info_key_list = info.xpath('dt/text()').extract()
            info_value_list = info.xpath('dd/p/text()|dd/text()').extract()
            for i in range(len(info_key_list)):
                info_key = "".join(info_key_list[i].split())
                info_value = info_value_list[i].split()
                info_dict[info_key] = info_value

        key_pair = [("用户评分", "score"),
                    ("国别", "country"),
                    ("影片类型", "type_info"),
                    ("更多外文名", "foreign_name"),
                    ("时长", "duration"),
                    ("色彩", "color"),
                    ("版本", "dimension"),
                    ("片名", "name_varify"),
                    ("上映信息", "playdate")]

        for info_key, info_eng in key_pair:
            if info_key in info_dict:
                if info_dict[info_key]:
                    item[info_eng] = info_dict[info_key]
                else:
                    item[info_eng] = None
            else:
                item[info_eng] = None

        print("=" * 30)
        print("name", item["name"])
        print("movie_id", item["movie_id"])
        print("scenario", item["scenario"])
        print("feature", item["feature"])
        print("make", item["make"])

        print("score", item["score"])
        print("country", item["country"])
        print("type_info", item["type_info"])
        print("foreign_name", item["foreign_name"])
        print("duration", item["duration"])
        print("color", item["color"])
        print("dimension", item["dimension"])
        print("name_varify", item["name_varify"])
        print("playdate", item["playdate"])

        print("url_video", item["url_video"])
        print("url_still", item["url_still"])
        print("url_news", item["url_news"])
        print("url_review", item["url_review"])
        print("url_performer", item["url_performer"])
        print("url_award", item["url_award"])
        print("url_scenario", item["url_scenario"])
        print("url_feature", item["url_feature"])
        print("url_make", item["url_make"])
        print("url_info", item["url_info"])

        return item
