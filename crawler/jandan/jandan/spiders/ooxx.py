# -*- coding: utf-8 -*-
import scrapy
import pymongo
import json
import pytz
from datetime import datetime, timedelta
from jandan.items import TucaoItem
import re

from scrapy.spidermiddlewares.httperror import HttpError


class OoxxSpider(scrapy.Spider):
    name = 'ooxx'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/']
    prefix = 'http://jandan.net/tucao/all/'
    count = 0
    
    def __init__(self):
        uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri)
        db = client.code
        comments = db.comments
        cn_time = datetime.now(pytz.timezone('Asia/Shanghai'))
        self.now = cn_time.strftime("%Y-%m-%d %H:%M:%S")
        past = (cn_time - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")
        self.result = comments.find({"time": {"$gt": past}}).sort('time', pymongo.DESCENDING)
        client.close()
    
    def start_requests(self):
        for item in self.result:
            id = item['pid']
            url = self.prefix + str(id)
            yield scrapy.Request(url, callback=self.parse,
                                 errback=self.error_callback,
                                 dont_filter=True)
    
    def parse(self, response):
        item = TucaoItem()
        text = json.loads(response.body)
        item['hot_tucao'] = text['hot_tucao']
        item['tucao'] = text['tucao']
        item['pid'] = int(re.search(r'\d+$', response.url).group())
        item['time'] = self.now
        yield item
    
    def error_callback(self, failure):
        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
