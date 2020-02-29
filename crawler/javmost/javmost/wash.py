import pymongo

prefix = "https://www5.javmost.com/{}/"
client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client.javmost
result = db.list.find({'url': {'$regex': "metastead.com"}})
for i in result:
    code = i['code']
    db.list.update_many({'code': code}, {'$set': {'url': prefix.format(code)}})
client.close()