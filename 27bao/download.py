import json
import urllib

def simple_download():
	fo = open("test.txt", "r+")
	line = fo.readlines()
	for i in range(0,len(line)):
		js = json.loads(line[i])
		for j in range(0,len(js["images"])):
			url = str(js["images"][j][0])
			print url
			name = str(j) + "s" + str(i) + ".gif"
			urllib.urlretrieve(url, name)
	fo.close()

simple_download()