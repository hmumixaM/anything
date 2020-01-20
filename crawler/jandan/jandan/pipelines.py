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
            print('Successful: ' + item['pid'])
            return item
        else:
            return item
    
    def categorize(self, item, comment):
        item['pid'] = comment['comment_ID']
        item['name'] = comment['comment_author']
        item['oo'] = comment['vote_positive']
        item['xx'] = comment['vote_negative']
        item['content'] = re.sub(r'/mw\d+/', '/large/', comment['comment_content'])
        item['time'] = comment['comment_date']
        return item


class PagePiepline(object):
    def process_item(self, item, spider):
        if isinstance(item, PageItem):
            item['time'] = self.time_normalization(item['time'])
            print(item)
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
        client = pymongo.MongoClient(host='127.0.0.1', port=27017)
        db = client.jandan
        self.comments = db.tucao
        self.collection = db.comments
    
    def process_item(self, item, spider):
        if isinstance(item, TucaoItem):
            result = self.comments.insert_one(dict(item))
            return item
        else:
            if not self.collection.find_one({'pid': item['pid']}):
                result = self.collection.insert_one(dict(item))
            return item
