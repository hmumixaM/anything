import cfscrape
import json

scraper = cfscrape.create_scraper()
a = json.loads(scraper.get("https://www5.javmost.com/showlistcate/all/1/allcode/").content)
print(a['status'])
print(a['data'])