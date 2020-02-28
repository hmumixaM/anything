import cfscrape

scraper = cfscrape.create_scraper()
with open('b.html', 'w') as file:
    file.write(scraper.get("https://www5.javmost.com/MOND-183/").text)