import pymongo

prefix = "https://www5.javmost.com/{}/"
client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client.javmost
count = 0
result = db.list.find({})
for i in result:
    if "javmost" not in i['url']:
        count += 1
        code = i['code']
        db.list.update_many({'code': code}, {'$set': {'url': prefix.format(code)}})
print(count)
client.close()