# -*- coding: utf-8 -*-
import scrapy
import pymongo
import re, json
import requests
from javmost.items import LinkItem

class ListSpider(scrapy.Spider):
    name = 'list'
    allowed_domains = ['www5.javmost.com']
    
    def __init__(self):
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.javmost
        self.result = db.list.find({})
        client.close()
        
    def start_requests(self):
        for item in self.result:
            link = item['url']
            yield scrapy.Request(link, callback=self.parse)

    def parse(self, response):
        item = LinkItem()
        item['url'] = response.url
        item['link'] = []
        url = "https://www5.javmost.com/get_movie_source/"
        pattern = re.compile(r"var YWRzMQo = .*?;")
        function = re.compile(r'''onclick="select_part\(.+?\)''')
        form = {}
        print(item['url'])
        form["value"] = pattern.search(response.text)[0][15:-2]
        print(form['value'])
        form["sound"] = 'av'
        select_part = function.findall(response.text)
        for i in select_part:
            parts = i.split(',')
            print(parts[1])
            form["part"] = parts[0][22:-1]
            form["group"] = parts[1][1:-1]
            form["code"] = parts[4][1:-1]
            form["code2"] = parts[5][1:-1]
            form["code3"] = parts[6][1:-2]
            response = requests.post(url, data=form)
            link = json.loads(response.text)['data'][0]
            item['link'].append(link)
        yield item