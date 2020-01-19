# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JandanItem(scrapy.Item):
    comment = scrapy.Field()
    security = scrapy.Field()
    id = scrapy.Field()
    content = scrapy.Field()
    xx = scrapy.Field()
    oo = scrapy.Field()
    name = scrapy.Field()
