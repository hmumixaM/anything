# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import requests

class JavmostPipeline(object):
    def __init__(self):
        uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri)
        # client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.javmost
        self.list = db.av
        self.count = 0
        self.total = 0
    
    def process_item(self, item, spider):
        if item["title"] == "Crawled":
            return 0
        else:
            a = self.list.find_one({'code': item['code']})
            if not a:
                self.count += 1
                result = self.list.insert_one(dict(item))
                print("Inserted {}".format(item['code']))
        if self.count == 1000:
            self.total += 1000
            requests.post("http://sc.ftqq.com/SCU72004T10f9864d58946bb2bb99613bef2ab8f75e023341e73f2.send",
                data={"text": "Another 1000 Pages: " + str(self.total), "desp": "nothing" + str(self.total)})
            self.count = 0
