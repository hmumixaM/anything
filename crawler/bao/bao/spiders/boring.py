# -*- coding: utf-8 -*-
import scrapy
from bao.items import BaoItem


class GifSpider(scrapy.Spider):
    name = 'boring'
    allowed_domains = ['m.27bao.com']
    
    def start_requests(self):
        prefix = "https://m.27bao.com/gaoxiaotupian/list_{}.html"
        for i in range(1, 391):
            url = prefix.format(i)
            yield scrapy.Request(url, callback=self.page)
    
    def page(self, response):
        items = response.xpath("//article[@class='post']")
        for item in items:
            obj = BaoItem()
            obj['title'] = item.xpath("div[1]/h2/a/text()").extract_first()
            obj['url'] = item.xpath("div[1]/h2/a/@href").extract_first()
            obj['link'] = item.xpath("div[2]/a/img/@src").extract_first()
            yield obj