# -*- coding: utf-8 -*-
import scrapy
from bao.items import BaoItem


class GifSpider(scrapy.Spider):
    name = 'gif'
    allowed_domains = ['m.27bao.com']
    
    def start_requests(self):
        prefix = "https://m.27bao.com/gif/list_{}.html"
        for i in range(1, 90):
            url = prefix.format(i)
            yield scrapy.Request(url, callback=self.page)
    
    def page(self, response):
        items = response.xpath("//article[@class='post']")
        for item in items:
            obj = BaoItem()
            obj['title'] = item.xpath("div[1]/h2/a/text()").extract_first()
            obj['url'] = item.xpath("div[1]/h2/a/@href").extract_first()
            yield scrapy.Request(obj['url'], callback=self.parse, meta={"item": obj})
    
    def parse(self, response):
        prefix = response.url[0:-5] + "_{}.html"
        obj = response.meta['item']
        obj['link'] = []
        
        obj['link'].append(response.xpath("//img/@src").extract()[1])
        max_page = response.xpath("//div[@class='paging']/span/text()").extract_first()
        max_page = int(max_page[0:-1].split('/')[1])
        
        yield scrapy.Request(prefix.format(2),
                             callback=self.img,
                             meta={'item': obj, 'max_page': max_page, 'order': 2, "prefix": prefix})
    
    def img(self, response):
        prefix = response.meta['prefix']
        obj = response.meta['item']
        max_page = response.meta['max_page']
        order = response.meta['order']
        obj['link'].append(response.xpath("//img/@src").extract()[1])
        
        print(obj['url'])
        
        if order < max_page:
            yield scrapy.Request(prefix.format(order + 1),
                                 callback=self.img,
                                 meta={'item': obj, 'max_page': max_page, 'order': order + 1, "prefix": prefix})
        if order == max_page:
            print(obj['link'])
            yield obj
