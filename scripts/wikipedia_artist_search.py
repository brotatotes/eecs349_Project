import requests, re, os
from bs4 import BeautifulSoup, SoupStrainer
import parse as p

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

def yahoo_search_bday(query):
	url = "https://search.yahoo.com/search?p=" + query
	print url
	html_doc = persistent_request(url)
	page = BeautifulSoup(html_doc.content, "html.parser")
	bday = page.find_all('span', {'class' : ' fz-4xl fc-first fw-s lh-m'})
	return str(bday)

def clean_up_yahoo_bday(bday):
	bday = bday.split(', ', 1)[-1]
	bday = re.sub(r'\<[^>]*\>', '', bday)
	bday = bday.split(' ', 1)[0]
	return bday

def wiki_search_bday(query):
	url = "https://en.wikipedia.org/wiki/" + query
	print url
	html_doc = persistent_request(url)
	page = BeautifulSoup(html_doc.content, "html.parser")
	bday = page.find_all('span', {'class' : 'bday'})
	return str(bday)

def clean_up_wiki_bday(bday):
	bday = bday.split('-', 1)[0]
	bday = re.sub(r'\<[^>]*\>', '', bday)
	bday = bday.split('[', 1)[1]
	bday = bday.split(']', 1)[0]
	return bday

songs_years = p.parse("../data/years.csv")
songs_artist = p.parse("../data/artists.csv")
songs_list = p.parse("../data/song_titles.csv")
song_data_headers = ["song", "artist", "age"]
ages = []
for i in range(5399):
	query = songs_artist[i]
	bday = wiki_search_bday(query)
	print bday
	if "bday dtstart" in bday:
		ages.append("?")
	elif bday != "[]":
		bday = clean_up_wiki_bday(bday)
		if "s" in bday:
			bday = bday.split('s', 1)[0]
			print bday
		ages.append(int(songs_years[i]) - int(bday))
	else:
		query = songs_artist[i] + " birthday"
		bday = yahoo_search_bday(query)
		bday = clean_up_yahoo_bday(bday)
		if bday != "[]":
			if "[" in bday:
				bday = bday.split('[', 1)[1]
			print bday
			ages.append(int(songs_years[i]) - int(bday))
		else:
			ages.append("?")
	print i

filename = "ages.csv"
file = open(filename, "w")
file.write(",".join(song_data_headers)+"\n")
for i in range(5399):
	file.write(str(songs_list[i]) + "," + str(songs_artist[i]) + "," + str(ages[i]) + "\n")
file.close()
