import requests
import json

prefix = 'http://jandan.net/t/'
count = 4471280
num = 0
for i in range(200):
    count -= 1
    response = requests.get(prefix + str(count))
    print(prefix + str(count))
    print(response.status_code)
    if (response.status_code == 404):
        num += 1

print(num)