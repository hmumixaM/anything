# -*- coding: utf-8 -*-
import scrapy


class VoteSpider(scrapy.Spider):
    name = 'vote'
    allowed_domains = ['i.jandan.net']
    start_urls = ['http://i.jandan.net/']

    def parse(self, response):
        pass
