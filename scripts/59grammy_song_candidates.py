import requests, re, os
from bs4 import BeautifulSoup, SoupStrainer

def persistent_request(url):
	"""Function that makes up to 10 api calls and returns the json object"""
	call_attempts = 0
	call_succeeded = False
	while (not call_succeeded) and (call_attempts < 10):
		try:
			html_doc = requests.get(url)
			return html_doc
		except:
			call_attempts += 1
	print "damn"
	return


html_doc = persistent_request("http://www.billboard.com/charts/hot-100/2016-05-21")
soup = BeautifulSoup(html_doc.text, 'html.parser')




