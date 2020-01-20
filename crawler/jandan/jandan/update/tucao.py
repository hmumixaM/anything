import pymongo
import requests
import json
import pytz
from datetime import datetime, timedelta

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client.jandan
collection = db.tucao

prefix = 'http://jandan.net/tucao/all/'

CNTime = datetime.now(pytz.timezone('Asia/Shanghai'))
now = CNTime.strftime("%Y-%m-%d %H:%M:%S")
past = (CNTime - timedelta(days=3)).strftime("%Y-%m-%d %H:%M:%S")

result = db.comments.find ({"time":{"$gt": past}})
for item in result:
    id = item['pid']
    print(id)
    url = prefix + str(id)
    response = json.loads(requests.get(url).content)
    response['id'] = id
    response['time'] = now
    del response['code']
    collection.insert_one(dict(response))