import pymongo
import requests
from time import sleep
from lxml import etree
from datetime import datetime


def db(item):
    uri = "mongodb+srv://hello:qweasdZxc1@jandan-l7bmq.gcp.mongodb.net/code?retryWrites=true&w=majority"
    client = pymongo.MongoClient(uri)
    db = client.code
    collection = db.h
    result = collection.insert_one(item)
    return result

def downloader(url):
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        response = requests.get(url, timeout=3)
        return response
    except requests.exceptions.ConnectTimeout:
        with open('error.log', 'a') as file:
            file.write(time + ": TimeOutError at " + url + '\n')
        return 'error'
    except requests.exceptions.ConnectionError:
        with open('error.log', 'a') as file:
            file.write(time + ": ConnectionError at " + url + '\n')
        return 'error'
    except Exception as e:
        with open('error.log', 'a') as file:
            file.write(time + ": Error at " + str(e) + '\n')
        return 'error'


def parse(response):
    content = etree.HTML(response.text)
    item = {}
    item['name'] = content.xpath('//div[@class="entry"]/b/text()')
    item['pid'] = int(content.xpath(response.url[22:]))
    images = content.xpath('//div[@class="entry"]/p/a/@href')
    text = content.xpath('//div[@class="entry"]/p/text()')
    if images:
        tracker = 0
        shift = 0
        for i in range(len(text)):
            if tracker == len(images) - 1 or shift + i == len(text):
                break
            if text[i + shift] != '\n':
                shift += 1
            else:
                text[i + shift] = images[tracker]
                tracker += 1
        text.append(images[-1])
    item['content'] = text
    print(item)
    return item


def init():
    count = 0
    pause = 0.5
    start = 4472182
    prefix = "http://i.jandan.net/t/"
    while True:
        url = prefix + str(start)
        sleep(pause)
        response = downloader(url)
        if response == 'error':
            continue
        print(start)
        print(response.status_code)
        if response.status_code == 404:
            count += 1
            start += 1
        elif response.status_code == 200:
            start += 1
            count = 0
            pause = 0.5
            item = parse(response)
            # db(item)
        else:
            sleep(1)
            continue
        if count == 10:
            print('reach the limit')
            start -= 10
            count = 0
            pause *= 2
    

def unit_test():
    prefix = "http://i.jandan.net/t/"
    num = 4472182
    response = requests.get(prefix + str(num))
    parse(response)


if __name__ == '__main__':
    init()
