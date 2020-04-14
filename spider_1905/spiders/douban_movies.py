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


def website_lookup(current_website, item_dict):
    website_sequence = ["movie_url", "url_performer", "url_scenario", "url_feature", "url_make", "url_info"]
    current_index = website_sequence.index(current_website)
    for website in website_sequence[current_index + 1:]:
        if item_dict[website] is not None:
            return website

    return False


class DoubanMovieSpider(scrapy.Spider):
    name = 'spider_1905'
    allowed_domains = ['1905.com']

    def start_requests(self):
        country_list = ["India"]
        # year_list = list(range(2014, 2021))
        year_list = [2014]
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

        # next_page = response.xpath('//div[@id="new_page"]/a[contains(text(),"下一页")]/@href').extract_first()
        # if next_page:
        #     next_page = "https://www.1905.com" + next_page
        #     print(f"Starting process website: {next_page}")
        #     yield scrapy.Request(url=next_page, callback=self.parse)
        # else:
        #     print("Congratulations!!!!")

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

        website = website_lookup(current_website="movie_url", item_dict=item)
        generated_callback = self.website_callback_generation(website)
        if generated_callback is not False:
            yield Request(url=item[website], meta={'item': item},
                          callback=generated_callback)
        else:
            return item

    def parse_movie_performer(self, response):
        item = response.meta['item']
        performer_dict = {}
        performers_1 = response.xpath('//div[contains(@class,"secPage-actors")]')
        for performer in performers_1:
            performer_key = performer.xpath('h3/text()').extract_first()
            if performer_key in ["导演", "编剧", "演员"]:
                # print("*" * 10, performer_key, "*" * 10)
                name_list_str = ""
                # print(performer)
                # performer_complete = performer.xpath('div[contains(@class,"secPage-actors-proList")]')
                # print(performer_complete)
                for info_content in performer.xpath('div/div/ul/li[contains(@class,"proList-conts-name")]'):
                    name = info_content.xpath('a/text()').extract_first()
                    name_eng = info_content.xpath('em/text()').extract_first()
                    name_full = f"{name}_{name_eng}"
                    name_list_str = name_full if name_list_str is "" else f"{name_list_str}|{name_full}"
                    # print(name_full)
                # print(name_list_str)
                performer_dict[performer_key] = name_list_str

        performers_2 = response.xpath('//div[contains(@class,"actors-producer-conts")]')
        for performer in performers_2:
            performer_key = performer.xpath('h3/text()').extract_first()
            performer_key = ''.join(performer_key.split())
            # print(performer_key)
            if performer_key in ["制片", "摄影", "剪辑", "原创音乐", "艺术指导", "副导演", "特技师"]:
                # print("*" * 10, performer_key, "*" * 10)
                name_list_str = ""
                # TODO 需要解决跳过 url 流程
                for info_content in performer.xpath('ul/li/div[contains(@class,"conts-name-top")]'):
                    name = info_content.xpath('a/text()').extract_first()
                    name_eng = info_content.xpath('em/text()').extract_first()
                    name_full = f"{name}_{name_eng}"
                    name_list_str = name_full if name_list_str is "" else f"{name_list_str}|{name_full}"
                performer_dict[performer_key] = name_list_str

        key_pair = [("导演", "director"),
                    ("编剧", "playwright"),
                    ("演员", "actor"),
                    ("制片", "producer"),
                    ("摄影", "photographer"),
                    ("剪辑", "montage"),
                    ("原创音乐", "music"),
                    ("艺术指导", "art_director"),
                    ("副导演", "assistant_director"),
                    ("特技师", "acrobats")]

        for info_key, info_eng in key_pair:
            if info_key in performer_dict:
                if performer_dict[info_key]:
                    item[info_eng] = performer_dict[info_key]
                else:
                    item[info_eng] = None
            else:
                item[info_eng] = None

        # yield Request(url=item["url_scenario"], meta={'item': item},
        #               callback=self.parse_movie_scenario)

        website = website_lookup(current_website="url_performer", item_dict=item)
        generated_callback = self.website_callback_generation(website)
        if generated_callback is not False:
            yield Request(url=item[website], meta={'item': item},
                          callback=generated_callback)
        else:
            return item

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

        # if item["url_feature"]:
        #     yield Request(url=item["url_feature"], meta={'item': item},
        #                   callback=self.parse_movie_feature)

        website = website_lookup(current_website="url_scenario", item_dict=item)
        generated_callback = self.website_callback_generation(website)
        if generated_callback is not False:
            yield Request(url=item[website], meta={'item': item},
                          callback=generated_callback)
        else:
            return item

    def parse_movie_feature(self, response):

        item = response.meta['item']

        feature = response.xpath('//dd/text()').extract()
        item["feature"] = feature

        # if item["url_make"]:
        #     yield Request(url=item["url_make"], meta={'item': item},
        #                   callback=self.parse_movie_make)

        website = website_lookup(current_website="url_feature", item_dict=item)
        generated_callback = self.website_callback_generation(website)
        if generated_callback is not False:
            yield Request(url=item[website], meta={'item': item},
                          callback=generated_callback)
        else:
            return item

    def parse_movie_make(self, response):
        item = response.meta['item']

        make = response.xpath('//dd[@class="icon_all"]/text()').extract()
        item["make"] = make

        # if item["url_info"]:
        #     yield Request(url=item["url_info"], meta={'item': item},
        #                   callback=self.parse_movie_info)

        website = website_lookup(current_website="url_make", item_dict=item)
        generated_callback = self.website_callback_generation(website)
        if generated_callback is not False:
            yield Request(url=item[website], meta={'item': item},
                          callback=generated_callback)
        else:
            return item

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

        print(item)
        return item

    def website_callback_generation(self, website):
        if website == "url_performer":
            return self.parse_movie_performer
        elif website == "url_scenario":
            return self.parse_movie_scenario
        elif website == "url_feature":
            return self.parse_movie_feature
        elif website == "url_make":
            return self.parse_movie_make
        elif website == "url_info":
            return self.parse_movie_info
        raise Exception("There is no way to generate next callback, please check again.")
