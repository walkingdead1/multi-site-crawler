import re
import requests
import sys
from urllib.parse import urljoin
import json
#import socket

target_link = input("Enter the url to crawl")
#print("The provided url does not exist")

target_urls = []
allcontents = []

def extrat_links(url):
	try:
		response = requests.get(url)
	except requests.exceptions.MissingSchema:
		print("the given url does not contain the proper schema(e.g http or https)")
		sys.exit(0)	
	except requests.exceptions.InvalidURL:
		print("The given url is Invalid")
		sys.exit(0)	
	except requests.exceptions.ConnectionError:
		print("A Connection error has occured please try sometime later")
		sys.exit(0)		
	href_links = re.compile(r'(?:href=")(.*?)"')
	g = href_links.findall(str(response.content))
	return g

def extract_contents(url):	
	response = requests.get(url)
	href_content = re.compile(r'<p>.*</p>')
	h = href_content.findall(str(response.content),re.DOTALL)
	return h

def crawl(url):
	for link in extrat_links(url):
		link = urljoin(url,link)
		
		if "#" in link:
			link = link.split("#")[0]

		if 	target_link in link and link not in target_urls:
			target_urls.append(link)
			allcontents.append({"page":str(link),"content":str(extract_contents(link))})
			crawl(link)
			

#print("contents:")
#for elements in extract_contents(target_link):
#	print(elements)
crawl(target_link)
#print(allcontents)
g = {"pages":allcontents}
print(json.dumps(g,ensure_ascii=False))


