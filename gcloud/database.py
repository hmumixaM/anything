import pymongo

uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
# client = pymongo.MongoClient(host='127.0.0.1', port=27017)
collection = client.anything.gif
# collection = client.baola.gif
jav = client.javmost.list
comments = client.code.comments
k = client.code.k
tucao = client.code.tucao
db_dict = {"tucao": tucao, "k": k, "comments": comments, "jav": jav, "gif": collection}


def find_gif(page):
    a = collection.find({})
    return a[page], a.count()


def find_javmost(page):
    a = jav.find({'videos': {"$exists": True}})
    return a[12*(page-1):12*page], a.count()


def find_video(code):
    result = jav.find_one({'code': code})
    if result['videos'] == []:
        return "error"
    return result


def restful(db, code):
    if (code == "count"):
        return db_dict[db].count()
    elif (code == "sort"):
        json = []
        result = db_dict[db].find({}).sort("$natural", pymongo.DESCENDING).limit(5)
        for i in result:
            json.append(dict(i))
        return str(json)
    else:
        return "You are wrong"


if __name__ == '__main__':
    a = find_gif(1)
    b = find_javmost(1)
    print(b[5])
