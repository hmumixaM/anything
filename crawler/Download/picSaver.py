import requests
import pymongo
import re
import os

# uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
# client = pymongo.MongoClient(uri)
client = pymongo.MongoClient(host='127.0.0.1', port=27017)
comments = client.jandan.comments
result = comments.find({'type': 'ooxx'}).sort('oo', pymongo.DESCENDING).limit(5000)

pattern = re.compile(r'http.*\.\w+')
suffix = re.compile(r'\.\w+$')

count = 0
num = 1
perDirLimit = 200
saveDir = 'img/Class_1'
os.makedirs(saveDir)
for rank in result:
    url = pattern.search(rank['content'])[0]
    img = requests.get(url, allow_redirects=False)
    if img.status_code == 301:
        continue
    if not count < perDirLimit:
        count = 0
        num += 1
        saveDir = 'img/Class_' + str(num)
        os.makedirs(saveDir)
    pathName = saveDir + "/{:03d}".format(count) + suffix.search(url)[0]
    with open(pathName, 'ab') as f:
        f.write(img.content)
    count += 1