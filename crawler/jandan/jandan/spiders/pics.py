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
    start_urls = ['http://i.jandan.net/pic/', 'http://i.jandan.net/treehole/', 'http://i.jandan.net/zoo/',
                  'http://i.jandan.net/qa/', 'http://i.jandan.net/ooxx/']
    
    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                 errback=self.error_callback,
                                 dont_filter=True)
    
    def parse(self, response):
        cn_time = datetime.now(pytz.timezone('Asia/Shanghai'))
        prefix = str(cn_time.year) + str(cn_time.month) + str(cn_time.day)
        total_page = response.xpath('//*[@id="comments"]/p[@class="wp-pagenavi"]/span/text()').extract_first()
        if 'pic' in response.url:
            url = 'http://i.jandan.net/?oxwlxojflwblxbsapi=jandan.get_pic_comments&page='
            for n in range(int(total_page[1:-1])):
                # for n in range(1, 2):
                yield scrapy.Request(url + str(n), callback=self.parse_json,
                                     errback=self.error_callback,
                                     dont_filter=True)
        elif 'ooxx' in response.url:
            url = 'http://i.jandan.net/?oxwlxojflwblxbsapi=jandan.get_ooxx_comments&page='
            for n in range(int(total_page[1:-1])):
                # for n in range(1, 2):
                yield scrapy.Request(url + str(n), callback=self.parse_json,
                                     errback=self.error_callback,
                                     dont_filter=True)
        else:
            for n in range(int(total_page[1:-1])):
                # for n in range(1, 2):
                url = response.url + '/' + base64.b64encode((prefix + '-' + str(n)).encode('utf-8')).decode('utf-8')
                yield scrapy.Request(url, callback=self.page_parse,
                                     errback=self.error_callback,
                                     dont_filter=True)
    
    def parse_json(self, response):
        item = JsonItem()
        text = json.loads(response.body)
        pic_type = response.url[51:54]
        for i in range(text['count']):
            item['type'] = pic_type
            item['content'] = text['comments'][i]
            yield item
    
    def page_parse(self, response):
        item = PageItem()
        with open("hel.html", 'w') as file:
            file.write(response.text)
        comment_list = response.xpath('//div[@id="comments"]/ol/li')
        pic_type = response.url[20:22]
        print(len(comment_list))
        for comment in comment_list:
            item['type'] = pic_type
            item['name'] = comment.xpath('b/text()').extract_first()
            item['pid'] = int(comment.xpath('span[@class="righttext"]/a/text()').extract_first())
            item['oo'] = int(comment.xpath('div[@class="jandan-vote"]/span[2]/span/text()').extract_first())
            item['xx'] = int(comment.xpath('div[@class="jandan-vote"]/span[3]/span/text()').extract_first())
            item['content'] = comment.xpath('div[@class="commenttext"]/p').extract_first()
            item['time'] = comment.xpath('span[@class="time"]/text()').extract_first()[1:-3]
            yield item
    
    def error_callback(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
