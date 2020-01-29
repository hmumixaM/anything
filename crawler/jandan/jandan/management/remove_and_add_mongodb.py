import json
import re
from datetime import timedelta, datetime
import pymongo
import pytz
import requests

# cn_time = datetime.now(pytz.timezone('Asia/Shanghai'))
# now = cn_time.strftime("%Y-%m-%d %H:%M:%S")
# past = (cn_time - timedelta(days=10)).strftime("%Y-%m-%d %H:%M:%S")

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client.jandan
tucao = db.tucao
comments = db.comments

posts = comments.find({'time': {'$gt': '2020-01-01 16:14:04'}})
print(posts)

for item in posts:
    a = item['pid']
    item['xx'] = int(item['xx'])
    item['oo'] = int(item['oo'])
    result = comments.replace_one({'pid': a}, item)
    print(result)

# list = [] # list of pid need to be removed
# prefix = '' # hyperlink prefix here
#
# for i in list:
#     print(i)
#     result = tucao.delete_many({'pid': i})
#     item = {}
#     response = requests.get(prefix + str(i))
#     text = json.loads(response.content)
#     item['hot_tucao'] = text['hot_tucao']
#     item['tucao'] = text['tucao']
#     item['pid'] = int(re.search(r'\d+$', response.url).group())
#     item['time'] = now
#     result = tucao.update_one(item)
