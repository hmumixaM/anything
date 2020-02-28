import cfscrape

scraper = cfscrape.create_scraper()
with open('a.html', 'w') as file:
    file.write(scraper.get("http://javmost.com").text)