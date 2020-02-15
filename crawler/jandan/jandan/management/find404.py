import pymongo

uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
h = client.code.h
comments = client.code.comments

result = h.find_many({})
for i in result:
    a = comments.find_one({'pid': i['pid']})
    if not a:
        with open('404.txt', 'a') as file:
            file.write('pid: ' + i['pid'] + ' name: ' + i['name'] + '\ncontent: ' + i['content'] + '\n')
