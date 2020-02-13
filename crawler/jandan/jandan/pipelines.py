# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo, re
from jandan.items import JsonItem, PageItem, TucaoItem
from datetime import datetime, timedelta


class JandanPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JsonItem):
            item = self.categorize(item, item['content'])
            return item
        else:
            return item
    
    def categorize(self, item, comment):
        if item['type'] == 'oox':
            item['type'] = 'ooxx'
        item['pid'] = int(comment['comment_ID'])
        item['name'] = comment['comment_author']
        item['oo'] = int(comment['vote_positive'])
        item['xx'] = int(comment['vote_negative'])
        item['content'] = re.sub(r'/mw\d+/', '/large/', comment['comment_content'])
        item['time'] = comment['comment_date']
        return item


class PagePiepline(object):
    def process_item(self, item, spider):
        if isinstance(item, PageItem):
            if item['type'] == 'zo':
                item['type'] = 'zoo'
            elif item['type'] == 'tr':
                item['type'] = 'treehole'
            return item
        else:
            return item


class DatabasePipeline(object):
    def __init__(self):
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.jandan
        self.comments = db.tucao
        self.collection = db.comments
    
    def process_item(self, item, spider):
        if isinstance(item, TucaoItem):
            if not self.comments.find_one({'pid': item['pid']}):
                result = self.comments.insert_one(dict(item))
                print("Added Tucao: " + str(item['pid']))
                return item
            else:
                result = self.comments.replace_one({'pid': item['pid']}, dict(item))
                print("Updated Tucao: " + str(item['pid']))
                return item
        else:
            content = self.collection.find_one({'pid': int(item['pid'])})
            if not content:
                result = self.collection.insert_one(dict(item))
                print("Added Comment: " + str(item['pid']))
                return item
            else:
                content['pid'] = item['pid']
                content['oo'] = item['oo']
                content['xx'] = item['xx']
                result = self.collection.replace_one({'pid': item['pid']}, content)
                print("Updated Comment: " + str(item['pid']))
                return item