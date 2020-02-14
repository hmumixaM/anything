import pymongo

uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
# client = pymongo.MongoClient(host='127.0.0.1', port=27017)
db = client.anything
# db = client.baola
collection = db.gif

def find(page):
    a = collection.find({})
    return a[page]


if __name__ == '__main__':
    a = find(1)
