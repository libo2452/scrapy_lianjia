# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaHouseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    lianjia_id = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    unit_price = scrapy.Field()


class LianjiaHouseImageItem(scrapy.Item):
    lianjia_id = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
