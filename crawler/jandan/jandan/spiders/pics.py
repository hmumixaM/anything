# -*- coding: utf-8 -*-
import scrapy
from scrapy.spidermiddlewares.httperror import HttpError
import json



class PicsSpider(scrapy.Spider):
    name = 'pics'
    allowed_domains = ['jandan.net']
    start_urls = ['http://jandan.net/t/4447328', 'http://jandan.net/t/4447333', 'http://jandan.net/t/4447319']
    category = {'问答': 'http://jandan.net/api/comment/neighbor/88399/',
                '树洞': 'http://jandan.net/api/comment/neighbor/102312/',
                '动物园': 'http://jandan.net/api/comment/neighbor/5596/'}
    prefix = 'http://jandan.net/t/'
    
    def start_requests(self):
        for u in self.start_urls:
            yield scrapy.Request(u, callback=self.parse,
                                 errback=self.error_callback,
                                 dont_filter=True)
            
    def next_post(self, response):
        prev_id = json.loads(response.body_as_unicode())['data']['prev_id']
        yield scrapy.Request(self.prefix + str(prev_id),
                             callback=self.parse,
                             errback=self.error_callback,
                             dont_filter=True)
    
    def parse(self, response):
        # with open('zoo.html', 'wb') as f:
        #     f.write(response.body)
        title = response.xpath("//*[@id='content']/h1/text()").extract()
        category = title[0].split()[0]
        pid = title[0].split()[1][3:]
        author = response.xpath("//div[@id='comments']/div/b/text()").extract()
        posts = response.xpath("//div[@id='comments']/div/p").extract()
        print(category, pid, author, posts)
        yield scrapy.Request(self.category[category] + pid, callback=self.next_post)
        
    def error_callback(self, failure):
        # self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)
