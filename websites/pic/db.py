import pymongo, re, random

uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
# client = pymongo.MongoClient(host='127.0.0.1', port=27017)
client = pymongo.MongoClient(uri)
# ooxx = client.jandan.comments
ooxx = client.code.comments
result = ooxx.find({'type':'ooxx'}).sort('oo', pymongo.DESCENDING)


def db():
    num = random.randint(0, 500)
    pattern = re.compile(r'http.*\.\w+')
    gif = result[num]['content']
    url = pattern.search(gif)[0]
    return url
