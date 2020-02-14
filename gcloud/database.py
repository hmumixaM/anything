import pymongo

uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
db = client.anything
collection = db.gif

def find(page):
    a = collection.find()
    return a[page]
