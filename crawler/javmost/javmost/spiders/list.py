# -*- coding: utf-8 -*-
import scrapy


class ListSpider(scrapy.Spider):
    name = 'list'
    allowed_domains = ['javmost.com']
    start_urls = ['http://javmost.com/']

    def parse(self, response):
        pass
