# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class JavmostPipeline(object):
    def __init__(self):
        uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri)
        # client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.javmost
        self.list = db.list
    
    def process_item(self, item, spider):
        result = self.list.insert_one(dict(item))
        print("Inserted {}".format(item['code']))
