# -*- coding: utf-8 -*-
import scrapy


class AvSpider(scrapy.Spider):
    name = 'av'
    allowed_domains = ['javmost.com']
    start_urls = ['http://javmost.com/']

    def parse(self, response):
        pass
