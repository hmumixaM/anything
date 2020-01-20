# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JsonItem(scrapy.Item):
    pid = scrapy.Field()
    content = scrapy.Field()
    xx = scrapy.Field()
    oo = scrapy.Field()
    name = scrapy.Field()
    time = scrapy.Field()
    tucao = scrapy.Field()
    
class PageItem(scrapy.Item):
    pid = scrapy.Field()
    content = scrapy.Field()
    xx = scrapy.Field()
    oo = scrapy.Field()
    name = scrapy.Field()
    time = scrapy.Field()
    tucao = scrapy.Field()

class TucaoItem(scrapy.Item):
    pid = scrapy.Field()
    hot_tucao = scrapy.Field()
    tucao = scrapy.Field()
    time = scrapy.Field()
    
class OOXXItem(scrapy.Item):
    pid = scrapy.Field()
    oo = scrapy.Field()
    xx = scrapy.Field()