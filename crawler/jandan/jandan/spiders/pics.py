# -*- coding: utf-8 -*-
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
from datetime import datetime, timedelta
import pytz, json, base64, pymongo


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
        tzCN = pytz.timezone('Asia/Shanghai')
        CNTime = datetime.now(tzCN)
        prefix = str(CNTime.year) + str(CNTime.month) + str(CNTime.day)
        total_page = response.xpath('//*[@id="comments"]/div[2]/div/span/text()').extract()
        if 'pic' in response.url:
            url = 'http://i.jandan.net/?oxwlxojflwblxbsapi=jandan.get_pic_comments&page='
            # for n in range(int(total_page[0][1:-1])):
            for n in range(1, 2):
                yield scrapy.Request(url + str(n), callback=self.parse_json,
                                     errback=self.error_callback,
                                     dont_filter=True)
        # elif 'ooxx' in response.url:
        #     url = 'http://i.jandan.net/?oxwlxojflwblxbsapi=jandan.get_ooxx_comments&page='
        #     # for n in range(int(total_page[0][1:-1])):
        #     for n in range(1, 2):
        #         yield scrapy.Request(url + str(n), callback=self.parse_json,
        #                              errback=self.error_callback,
        #                              dont_filter=True)
        # else:
        #     # for n in range(int(total_page[0][1:-1])):
        #     for n in range(1, 2):
        #         url = response.url + '/' + base64.b64encode((prefix + '-' + str(n)).encode('utf-8')).decode('utf-8')
        #         yield scrapy.Request(url, callback=self.page_parse,
        #                              errback=self.error_callback,
        #                              dont_filter=True)
    
    def parse_json(self, response):
        text = json.loads(response.body)
        for i in range(text['count']):
            comment = text['comments'][i]
            id = comment['comment_ID']
            name = comment['comment_author']
            oo = comment['vote_positive']
            xx = comment['vote_negative']
            content = comment['comment_content']
            time = comment['comment_date']
    
    def page_parse(self, response):
        comment_list = response.xpath('//div[@id="comments"]/ol/li')
        for comments in comment_list:
            comment = comments.xpath('div/div')
            id = comment.xpath('div[2]/span/a/text()').extract_first()
            security = comment.xpath('div[1]/strong//@title').extract_first()[4:]
            name = comment.xpath('div[1]/strong/text()').extract_first()
            oo = comment.xpath('div[3]/span[2]/span/text()').extract_first()
            xx = comment.xpath('div[3]/span[3]/span/text()').extract_first()
            content = comment.xpath('div[2]/p').extract_first()
            time = comment.xpath('div[1]/small/a/text()').extract_first()[1:-3]
            if '周' in time:
                delta = timedelta(weeks=-1 * int(time[:-2]))
            elif '天' in time:
                delta = timedelta(days=-1 * int(time[:-2]))
            elif '小时' in time:
                delta = timedelta(hours=-1 * int(time[:-3]))
            elif '分钟' in time:
                delta = timedelta(minutes=-1 * int(time[:-3]))
            elif '秒' in time:
                delta = timedelta(seconds=-1 * int(time[:-2]))
            now = datetime.now()
            time = (now + delta).strftime('%Y-%m-%d %H:%M:%S')
            yield scrapy.Request('http://jandan.net/tucao/all/' + id,
                                 callback=self.comment_update,
                                 errback=self.error_callback,
                                 dont_filter=True)
    
    def comment_update(self, response):
        text = json.loads(response.body)
    
    def error_callback(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
