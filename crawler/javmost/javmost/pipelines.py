# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from javmost.items import ListItem

class JavmostPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.javmost
        self.list = db.list
    
    def process_item(self, item, spider):
        result = self.list.insert_one(dict(item))
        print("Inserted {}".format(item['code']))
