# -*- coding: utf-8 -*-
import re
import scrapy
import json
from javmost.items import ListItem

class AvSpider(scrapy.Spider):
    name = 'av'
    allowed_domains = ['www5.javmost.com']
    start_urls = 'https://www5.javmost.com/showlistcate/all/{}/allcode/'
    
    def start_requests(self):
        page_number = 1
        while page_number < 84:
            url = self.start_urls.format(page_number)
            page_number += 1
            yield scrapy.Request(url, callback=self.code_parse)
    
    def code_parse(self, response):
        data = json.loads(response.body)
        selector = scrapy.Selector(text=data['data'], type="html")
        codes = selector.xpath('//h4/text()').extract()
        prefix = "https://www5.javmost.com/code/{}/"
        urls = list(map(lambda x: prefix.format(x.split()[0]), codes))
        for link in urls:
            yield scrapy.Request(link, callback=self.code_request)
    
    def code_request(self, response):
        pattern = re.compile(r"page/\d+/\">&darr;")
        maximum_page = int(pattern.search(response.text)[0].split("/")[1])
        suffix = "https://www5.javmost.com/showlist/{}/{}/code/"
        code = response.url.split("/")[-2]
        for i in range(1, maximum_page + 1):
            link = suffix.format(code, i)
            yield scrapy.Request(link, callback=self.list_parse)
    
    def list_parse(self, response):
        data = json.loads(response.body)
        selector = scrapy.Selector(text=data['data'], type="html")
        cards = selector.xpath("//div[@class='card']")
        for card in cards:
            item = ListItem()
            item['image'] = card.xpath("a/img/@data-src").extract_first()
            item['code'] = card.xpath("div/a[1]/h4/text()").extract_first()
            item['url'] = card.xpath("div/a[1]/@href").extract_first()
            item['title'] = card.xpath("div/a[2]/h5/text()").extract_first()
            item['release_time'] = card.xpath("div/p/text()[2]").extract_first().split('\t')[0].split(" ")[-1]
            item['rating'] = card.xpath("div/p/text()[5]").extract_first().split('\t')[0].split(" ")[-1]
            item['duration'] = card.xpath("div/p/span/text()").extract_first()
            item['genre'] = card.xpath("div/p/a[@class='btn btn-warning btn-xs m-r-5 m-t-2']/text()").extract()
            item['star'] = card.xpath("div/p/a[@class='btn btn-danger btn-xs m-r-5 m-t-2']/text()").extract()
            item['maker'] = card.xpath("div/p/a[@class='btn btn-info btn-xs m-r-5 m-t-2']/text()").extract()
            item['director'] = card.xpath("div/p/a[@class='btn btn-success btn-xs m-r-5 m-t-2']/text()").extract()
            item['tags'] = card.xpath("div/p/a[@class='btn btn-inverse btn-xs m-r-5 m-t-2']/text()").extract()
            yield item