import pymongo

# uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
# client = pymongo.MongoClient(uri)
client = pymongo.MongoClient(host='127.0.0.1', port=27017)
# db = client.anything
db = client.baola
collection = db.gif
jav = client.javmost.list

def find_gif(page):
    a = collection.find({})
    return a[page]


def find_javmost(page):
    a = jav.find({'videos': {"$exists": True}})
    return a[0:10*page]

if __name__ == '__main__':
    a = find_gif(1)
    b = find_javmost(1)
    print(b[5])
