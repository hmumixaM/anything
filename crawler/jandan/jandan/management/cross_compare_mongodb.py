import pymongo

client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client.jandan
tucao = db.tucao
comments = db.comments

result = tucao.find({'pid': {'$gt': 1}})
b = 0
for i in result:
    if not comments.find_one({'pid': i['pid']}):
        print(i['pid'])
        b += 1
        print(b)
        
client.close()