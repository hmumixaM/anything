# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import requests


class BaoPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        self.new = client.baola.new
        self.counter = 0
        self.total = 0
    
    def process_item(self, item, spider):
        if not self.new.find_one({'url': item['url']}):
            self.new.insert_one(dict(item))
            print("Inserted {}".format(item['url']))
            self.counter += 1
        else:
            print("Duplicate {}".format(item['url']))
        if self.counter > 500:
            self.counter = 0
            self.total += 500
            requests.post("http://sc.ftqq.com/SCU72004T10f9864d58946bb2bb99613bef2ab8f75e023341e73f2.send",
                          data={"text": "27Bao Crawled {}".format(self.total), "desp": "Total is {}".format(self.total)})