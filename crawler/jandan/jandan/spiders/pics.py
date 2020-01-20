# -*- coding: utf-8 -*-
import base64
from datetime import datetime
from jandan.items import JsonItem, PageItem

import json
import pytz
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError


class PicsSpider(scrapy.Spider):
    name = 'pics'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/pic/', 'http://jandan.net/t/treehole/', 'http://jandan.net/t/zoo/',
                  'http://jandan.net/qa/', 'http://jandan.net/ooxx/']
    
    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                 errback=self.error_callback,
                                 dont_filter=True)
    
    def parse(self, response):
        cn_time = datetime.now(pytz.timezone('Asia/Shanghai'))
        prefix = str(cn_time.year) + str(cn_time.month) + str(cn_time.day)
        total_page = response.xpath('//*[@id="comments"]/div[2]/div/span/text()').extract()
        if 'pic' in response.url:
            url = 'http://i.jandan.net/?oxwlxojflwblxbsapi=jandan.get_pic_comments&page='
            for n in range(int(total_page[0][1:-1])):
                # for n in range(1, 2):
                yield scrapy.Request(url + str(n), callback=self.parse_json,
                                     errback=self.error_callback,
                                     dont_filter=True)
        elif 'ooxx' in response.url:
            url = 'http://i.jandan.net/?oxwlxojflwblxbsapi=jandan.get_ooxx_comments&page='
            for n in range(int(total_page[0][1:-1])):
                # for n in range(1, 2):
                yield scrapy.Request(url + str(n), callback=self.parse_json,
                                     errback=self.error_callback,
                                     dont_filter=True)
        else:
            for n in range(int(total_page[0][1:-1])):
                # for n in range(1, 2):
                url = response.url + '/' + base64.b64encode((prefix + '-' + str(n)).encode('utf-8')).decode('utf-8')
                yield scrapy.Request(url, callback=self.page_parse,
                                     errback=self.error_callback,
                                     dont_filter=True)
    
    def parse_json(self, response):
        item = JsonItem()
        text = json.loads(response.body)
        for i in range(text['count']):
            item['content'] = text['comments'][i]
            yield item
    
    def page_parse(self, response):
        item = PageItem()
        comment_list = response.xpath('//div[@id="comments"]/ol/li')
        for comments in comment_list:
            comment = comments.xpath('div/div')
            item['pid'] = comment.xpath('div[2]/span/a/text()').extract_first()
            item['name'] = comment.xpath('div[1]/strong/text()').extract_first()
            item['oo'] = comment.xpath('div[3]/span[2]/span/text()').extract_first()
            item['xx'] = comment.xpath('div[3]/span[3]/span/text()').extract_first()
            item['content'] = comment.xpath('div[2]/p').extract_first()
            item['time'] = comment.xpath('div[1]/small/a/text()').extract_first()[1:-3]
            yield item
    
    def error_callback(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
