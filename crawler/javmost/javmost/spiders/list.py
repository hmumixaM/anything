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
        uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri)
        # client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.javmost
        self.temp = client.javmost.temp
        self.result = db.list.find({'videos': {"$exists": False}}).sort("rating", pymongo.DESCENDING)
        
    def start_requests(self):
        count = 0
        for item in self.result:
            a = self.temp.find_one({'url': item['url']})
            if not a:
                if count == 0:
                    requests.post("http://sc.ftqq.com/SCU72004T10f9864d58946bb2bb99613bef2ab8f75e023341e73f2.send",
                        data={"text": "crawling first item: " + item['code'], "desp": item['url']})
                    count = 1
                link = item['url']
                yield scrapy.Request(link, callback=self.parse)

    def parse(self, response):
        item = LinkItem()
        item['url'] = response.url
        item['form'] = []
        url = "https://www5.javmost.com/get_movie_source/"
        pattern = re.compile(r"var YWRzMQo = .*?;")
        function = re.compile(r'''onclick="select_part\(.+?\)''')
        form = {}
        form["value"] = pattern.search(response.text)[0][15:-2]
        form["sound"] = 'av'
        select_part = function.findall(response.text)
        for i in select_part:
            parts = i.split(',')
            if parts[3][1:-1] == 'parent':
                continue
            form["part"] = parts[0][22:-1]
            form["group"] = parts[1][1:-1]
            form["code"] = parts[4][1:-1]
            form["code2"] = parts[5][1:-1]
            form["code3"] = parts[6][1:-2]
            # response = requests.post(url, data=form)
            # data = json.loads(response.text)
            # if not data['status'] == "error":
            #     item['link'] += data['data']
            item['form'] += [list(form.items())]
        yield item
