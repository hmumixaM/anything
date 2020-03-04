import pymongo
import requests

uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
temp = client.javmost.temp
db = client.javmost.list
result = temp.find({})

def download(data):
    prefix = "https://www5.javmost.com/get_movie_source/"
    link = []
    try:
        a = requests.post(prefix, data=data).json()
        if not a['status'] == "error":
            link = a['data']
    except Exception as e:
        requests.post("http://sc.ftqq.com/SCU72004T10f9864d58946bb2bb99613bef2ab8f75e023341e73f2.send",
                data={"text": "Javmost Video Spider Fail", "desp": str(e)})
    
    return link


count = 0
for item in result:
    link = []
    url = item['url']
    forms = item['form']
    for form in forms:
        data = dict(form)
        link.append(download(form))
    try:
        db.update_one({'url': url}, {'$set': {'videos': link}})
    except Exception as e:
        requests.post("http://sc.ftqq.com/SCU72004T10f9864d58946bb2bb99613bef2ab8f75e023341e73f2.send",
                data={"text": "Pymongo Error", "desp": str(e)})
    count += 1
    print(url)
    if count == 500:
        requests.post("http://sc.ftqq.com/SCU72004T10f9864d58946bb2bb99613bef2ab8f75e023341e73f2.send",
                data={"text": "Another 500 datapoints crawled", "desp": "nothing"})
        count = 0
