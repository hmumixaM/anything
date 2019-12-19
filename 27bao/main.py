# -*- coding: UTF-8 -*-

import re
import requests


# Recursion for webpages

def recursion():
	for i in range(34,39):
		list_link = "https://m.27baola.net/gif/list_"
		list_link = list_link + str(i) + ".html"
		page = requests.get(list_link)
		page.encoding = 'UTF-8'
		page_match(page)

# Identify links from webpages

def page_match(page):
	pattern = re.compile(r"href='/gif/\d{1,5}\.html' alt='.{4,30}'")
	result = pattern.findall(page.text)

	for i in range(0,len(result)):
		link_pattern = re.compile(r"/gif/\d{1,5}\.html")
		link = "https://m.27baola.net" + str(link_pattern.findall(result[i])[0])
		description_pattern = re.compile(r"alt='.{5,40}'")
		try:
			description = description_pattern.findall(result[i])[0]
			description = description[5:-1]
		except BaseException:
			description = "NoDescription"
			print "ERROR FOR DESCRITPION AT" + link
		#issue_pattern = re.compile(r"\s\d{2}.{10}")
		#order_pattern = re.compile(r"\d{1,4}")
		#try:
		#	issue = issue_pattern.findall(result[i])[0]
		#	order = order_pattern.findall(issue)[1]
		#except BaseException:
		#	order = "NoOrder"
		#	print "ERROR FOR ORDER AT" + link

		images = image_match(link)
		storage(link, description, images)


# Identify images from pages

def image_match(link):
	print link
	images = [] 

	html = requests.get(link)
	html.encoding = "UTF-8"
	image = image_find(html)
	images.append(image)
	next_link = next_page(html)
	while next_link != "end":
		html = requests.get(next_link)
		html.encoding = "UTF-8"
		image = image_find(html)
		images.append(image)
		next_link = next_page(html)

	return images


## Sub-function: image find

def image_find(page):
	pattern = re.compile(r"http://.{10,300}\.gif")
	image = pattern.findall(page.text)

	return image


## Sub-function: next page find

def next_page(page):
	pattern = re.compile(r"<a href='\d{1,5}_\d{1,2}.html'  id=\"btn\"")
	next_link = pattern.findall(page.text)
	if len(next_link) == 0:
		return "end"
	else:
		link_pattern = re.compile(r"\d{1,5}_\d{1,2}\.html")
		link = link_pattern.findall(next_link[0])[0]
		link = "https://m.27baola.net/gif/" + link
		return link


if __name__ == '__main__':
    recursion()