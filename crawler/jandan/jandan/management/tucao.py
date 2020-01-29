import requests
import json

prefix = 'http://jandan.net/tucao/all/'
for i in range(4430021, 1, -1):
    response = requests.get(prefix + str(i))
    text = json.loads(response.content)
    if len(text['tucao']) != 0:
        print(i)