import cfscrape
import json
import scrapy

scraper = cfscrape.create_scraper()
a = json.loads(scraper.get("https://www5.javmost.com/showlistcate/all/1/allcode/").content)
print(a['status'])
data = scrapy.Selector(text=a['data'], type='html')
