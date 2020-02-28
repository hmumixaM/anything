import requests
from faker import Faker
from fake_headers import Headers
import json

faker = Faker()
header = Headers()
comment_id = int(input("comment_id: "))
like_type = input("like_type: ")
data_type = input("data_type: ")
times = int(input("repeat times: "))
for _ in range(times):
        link = 'http://jandan.net/api/comment/vote'
        headers = header.generate()
        headers['origin'] = "https://jandan.net"
        headers['content-typ'] = "application/x-www-form-urlencoded; charset=UTF-8"
        ip = faker.ipv4()
        headers["X-Forwarded-For"] = ip
        headers["Client-IP"] = ip
        try:
            r = requests.post(link, data={"comment_id": comment_id, "like_type": like_type, "data_type": data_type},
                              headers=headers,
                              timeout=10)
            print(r.text)
        except TimeoutError:
            print("TimeOut")
        except Exception as e:
            print(str(e))
