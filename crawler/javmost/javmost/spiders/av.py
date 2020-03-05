# -*- coding: utf-8 -*-
import re
import scrapy
import json
import pymongo
from javmost.items import ListItem


class AvSpider(scrapy.Spider):
    name = 'av'
    allowed_domains = ['www5.javmost.com'] 
    
    def __init__(self):
        uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri)
        av = client.javmost.av
        self.database = []
        result = av.aggregate([{"$group": {"_id": {"code": "$code"}}}])
        for i in result:
            self.database.append(i['_id']["code"])
    
    def start_requests(self):
        suffix = "https://www5.javmost.com/showlist/new/{}/release/"
        for i in range(0, 4349):
            link = suffix.format(i)
            yield scrapy.Request(link, callback=self.list_parse)
    
    def list_parse(self, response):
        check(response)
        data = json.loads(response.body)
        selector = scrapy.Selector(text=data['data'], type="html")
        cards = selector.xpath("//div[@class='card']")
        for card in cards:
            item = ListItem()
            item['image'] = card.xpath("a/img/@data-src").extract_first()
            item['code'] = card.xpath("div/a[1]/h4/text()").extract_first()
            if item['code'] in self.database:
                item['title'] = "Crawled"
                continue
            item['url'] = "https://www5.javmost.com/{}/".format(item['code'])
            item['title'] = card.xpath("div/a[2]/h5/text()").extract_first()
            item['release_time'] = card.xpath("div/p/text()[2]").extract_first().split('\t')[0].split(" ")[-1]
            item['rating'] = card.xpath("div/p/text()[5]").extract_first().split('\t')[0].split(" ")[-1]
            item['duration'] = card.xpath("div/p/span/text()").extract_first()
            item['genre'] = card.xpath("div/p/a[@class='btn btn-warning btn-xs m-r-5 m-t-2']/text()").extract()
            item['star'] = card.xpath("div/p/a[@class='btn btn-danger btn-xs m-r-5 m-t-2']/text()").extract()
            item['maker'] = card.xpath("div/p/a[@class='btn btn-info btn-xs m-r-5 m-t-2']/text()").extract()
            item['director'] = card.xpath("div/p/a[@class='btn btn-success btn-xs m-r-5 m-t-2']/text()").extract()
            item['tags'] = card.xpath("div/p/a[@class='btn btn-inverse btn-xs m-r-5 m-t-2']/text()").extract()
            yield scrapy.Request(item['url'], callback=self.parse, meta={'item': item})
    
    def parse(self, response):
        check(response)
        url = "https://www5.javmost.com/get_movie_source/"
        item = response.meta['item']
        item['videos'] = []
        form = {}
        
        pattern = re.compile(r"var YWRzMQo = .*?;")
        function = re.compile(r'''onclick="select_part\(.+?\)''')
        form["value"] = pattern.search(response.text)[0][15:-2]
        form["sound"] = 'av'
        select_part = function.findall(response.text)
        
        i = select_part[-1]
        parts = i.split(',')
        form["part"] = parts[0][22:-1]
        form["group"] = parts[1][1:-1]
        form["code"] = parts[4][1:-1]
        form["code2"] = parts[5][1:-1]
        form["code3"] = parts[6][1:-2]
        
        yield scrapy.FormRequest(url,
                                 formdata=form,
                                 callback=self.form_requests,
                                 meta={"item": item,
                                       "num": len(select_part) - 1,
                                       "select_part": select_part,
                                       'form': form})
    
    def form_requests(self, response):
        check(response)
        item = response.meta['item']
        data = json.loads(response.text)
        if data['status'] == "success":
            item['videos'] += data['data']

        url = "https://www5.javmost.com/get_movie_source/"
        select_part = response.meta['select_part']
        num = response.meta['num']
        form = response.meta['form']

        if num > 0:
            i = select_part[num - 1]
            parts = i.split(',')
            form["part"] = parts[0][22:-1]
            form["group"] = parts[1][1:-1]
            form["code"] = parts[4][1:-1]
            form["code2"] = parts[5][1:-1]
            form["code3"] = parts[6][1:-2]
            yield scrapy.FormRequest(url,
                                     formdata=form,
                                     callback=self.form_requests,
                                     meta={"item": item,
                                           "num": num - 1,
                                           "select_part": select_part,
                                           'form': form})
        if num == 0:
            yield item

    def check(response):
        if response.status == 503:
            requests.post("http://sc.ftqq.com/SCU72004T10f9864d58946bb2bb99613bef2ab8f75e023341e73f2.send",
                    data={"text": "Javmost Video Spider Fail: 503", "desp": "503 ERROR"})
