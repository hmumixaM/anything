# -*- coding: utf-8 -*-
import scrapy


class PicsSpider(scrapy.Spider):
    name = 'pics'
    allowed_domains = ['jandan.net', '*.sinaimg.cn']
    start_urls = ['http://jandan.net/t/4440000']
    
    def parse(self, response):
        filename = "sinapic.html"
        open(filename, 'w').write(response.body)
