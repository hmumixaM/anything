# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ListItem(scrapy.Item):
    code = scrapy.Field()
    title = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()
    rating = scrapy.Field()
    star = scrapy.Field()
    genre = scrapy.Field()
    director = scrapy.Field()
    maker = scrapy.Field()
    tags = scrapy.Field()
    release_time = scrapy.Field()
    duration = scrapy.Field()
    videos = scrapy.Field()