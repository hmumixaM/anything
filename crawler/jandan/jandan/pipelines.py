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
            item['time'] = self.time_normalization(item['time'])
            if item['type'] == 'zo':
                item['type'] = 'zoo'
            elif item['type'] == 'tr':
                item['type'] = 'treehole'
            return item
        else:
            return item
    
    def time_normalization(self, time):
        if '周' in time:
            delta = timedelta(weeks=-1 * int(time[:-2]))
        elif '天' in time:
            delta = timedelta(days=-1 * int(time[:-2]))
        elif '小时' in time:
            delta = timedelta(hours=-1 * int(time[:-3]))
        elif '分钟' in time:
            delta = timedelta(minutes=-1 * int(time[:-3]))
        elif '秒' in time:
            delta = timedelta(seconds=-1 * int(time[:-2]))
        now = datetime.now()
        return (now + delta).strftime('%Y-%m-%d %H:%M:%S')


class DatabasePipeline(object):
    def __init__(self):
        uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
        client = pymongo.MongoClient(uri)
        db = client.code
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
