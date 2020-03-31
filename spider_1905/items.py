# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Spider1905Item(scrapy.Item):
    # define the fields for your item here like:

    movie_url = scrapy.Field()  # 电影主页

    url_video = scrapy.Field()  # 在线观看信息
    url_still = scrapy.Field()  # 图片
    url_news = scrapy.Field()  # 新闻
    url_review = scrapy.Field()  # 影评
    url_performer = scrapy.Field()  # 演职人员
    url_award = scrapy.Field()  # 获奖信息
    url_scenario = scrapy.Field()  # 剧情
    url_feature = scrapy.Field()  # 幕后花絮
    url_make = scrapy.Field()  # 机构信息
    url_info = scrapy.Field()  # 详细信息

    movie_id = scrapy.Field()  # 电影 ID
    name = scrapy.Field()  # 电影名称
    scenario = scrapy.Field()  # 电影剧情
    make = scrapy.Field()  # 机构信息
    feature = scrapy.Field()  # 幕后花絮
    score = scrapy.Field()  # 电影评分
    country = scrapy.Field()  # 国别信息
    type_info = scrapy.Field()  # 类别信息
    foreign_name = scrapy.Field()  # 更多外文名
    duration = scrapy.Field()  # 时长信息
    color = scrapy.Field()  # 色彩信息
    dimension = scrapy.Field()  # 版本信息
    name_varify = scrapy.Field()  # 二次验证片名，确保爬虫形成闭环
    playdate = scrapy.Field()  # 上映信息
