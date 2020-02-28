# -*- coding: utf-8 -*-
import scrapy
import json
from lxml import etree
from javmost.items import ListItem

class AvSpider(scrapy.Spider):
    name = 'av'
    allowed_domains = ['www5.javmost.com']
    start_urls = 'https://www5.javmost.com/showlistcate/all/{}/allcode/'
    
    def start_requests(self):
        page_number = 1
        while page_number==1:
            url = self.start_urls.format(page_number)
            page_number += 1
            yield scrapy.Request(url, callback=self.code_parse)
    
    def code_parse(self, response):
        data = json.load(response.body)
    
    def parse(self, response):
        with open("test.txt", 'a') as file:
            file.write(response.text)
