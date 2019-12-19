import requests
import re
import pymongo


def main():
    client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    db = client.baola
    collection = db.gif
    pages = list_link()
    for link in pages:
        gifs, description = gif_match(link)
        info = {"title": description, "gif": gifs}
        result = collection.insert_one(info)


def list_link():
    pages = []
    prefix = "https://www.27bao.com/gif/list_{}.html"
    for i in range(51):
        link = prefix.format(i)
        text = download(link)
        info = match(text, r"href='/gif/\d{1,5}\.html' alt='.{4,30}'")
        for item in info:
            location = "https://www.27bao.com"
            href = location + match(item, r"/gif/\d{1,5}\.html", "search")
            alt = match(item, r"alt='.{5,40}'", "search")[5:-1]
            pages.append([href, alt])
    fo = open("page.txt", "w")
    for i in pages:
        fo.write(i[0])
        fo.write("@")
        fo.write(i[1])
        fo.write("\n")
    fo.close()
    return pages


def gif_match(link):
    gifs = []
    href = link[0]
    description = link[1]
    text = download(href)
    text = match(text, r"<div id=\"pages\">.+</div>", "search")
    image_pages = match(text, r"href='\d{1,5}_\d{1,2}\.html'")
    for image in image_pages:
        location = "https://www.27bao.com/gif/{}"
        image = location.format(image[6:-1])
        image_text = download(image)
        info = match(image_text, r"<img alt=\".+\.gif", "search")
        gif_href = match(info, r"http.+\.gif", "search")
        gif_alt = match(info, r"alt=\".{5,40}\"", "search")[5:-1]
        gifs.append([gif_href, gif_alt])
    return gifs, description
    

def download(link):
    response = requests.get(link)
    response.encoding = "UTF-8"
    return response.text

    
def match(text, regex, mode="findall"):
    pattern = re.compile(regex)
    if mode == "findall":
        result = pattern.findall(text)
    elif mode == "search":
        result = pattern.search(text)[0]
    return result


if __name__ == '__main__':
    main()
