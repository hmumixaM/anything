# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class JavmostPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.test
        self.list = db.list
    
    def process_item(self, item, spider):
        item = self.list.find_one({"code": item["code"]})
        if not item:
            result = self.list.insert_one(dict(item))
            print("Inserted {}".format(item['code']))
        else:
            result = self.list.replace_one(dict(item))
            print("Updated {}".format(item['code']))
