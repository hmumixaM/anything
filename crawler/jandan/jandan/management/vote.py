import requests
from faker import Faker
from fake_headers import Headers

faker = Faker()
header = Headers()
for i in range(30):
    ip = faker.ipv4()
    headers = header.generate()
    headers["X-Forwarded-For"] = ip
    headers["Client-IP"] = ip
    r = requests.post('http://jandan.net/api/comment/vote', json={"id": "4450914", "vote_type": -1}, headers=headers)
    print(r.text)