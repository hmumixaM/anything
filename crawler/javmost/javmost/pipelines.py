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
<<<<<<< HEAD
        if isinstance(item, ListItem):
            result = self.list.insert_one(dict(item))
            print("Inserted {}".format(item['code']))


class LinkPipeline(object):
    def __init__(self):
        uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri)
        # client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.javmost
        # self.list = db.list
        self.list = db.temp
        
    def process_item(self, item, spider):
        if isinstance(item, LinkItem):
            print(item['url'])
            # self.list.update_one({'url': item['url']}, {'$set': {'videos': item['link']}})
            self.list.insert_one(dict(item))
            print("Updated {}".format(item['url']))
=======
        result = self.list.insert_one(dict(item))
        print("Inserted {}".format(item['code']))
>>>>>>> 719acac83420f73eedeb0662948362f7ed050774
