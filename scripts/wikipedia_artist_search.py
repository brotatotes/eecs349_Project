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
	html_doc = persistent_request(url)
	page = BeautifulSoup(html_doc.content)
	bday = page.find_all('span', {'class' : ' fz-4xl fc-first fw-s lh-m'})
	return str(bday)

def yahoo_search_members(query):
	url = "https://search.yahoo.com/search?p=" + query
	html_doc = persistent_request(url)
	page = BeautifulSoup(html_doc.content)
	members = page.find_all('ul', {'class' : 'compInfo mb-25'})
	return str(members)

def clean_up_birthday(bday):
	bday = bday.split(', ', 1)[-1]
	bday = re.sub(r'\<[^>]*\>', '', bday)
	bday = bday.split(' ', 1)[0]
	return bday

def clean_up_members(members):
	print members
	members = re.sub(r'\<[^>]*\>', '', members)
	print members
	members = members.split('[Members: ', 1)[1]
	member = members.split(',', 1)[0]
	return member

songs_years = p.parse("./years.csv")
songs_artist = p.parse("./artists.csv")
song_data_headers = ["song", "artist", "age"]
ages = []
for i in range(0,2):
	query = songs_artist[i] + " birthday"
	bday = yahoo_search_bday(query)
	bday = clean_up_birthday(bday)
	if bday != "[]":
		ages.append(int(songs_years[i]) - int(bday))
	else:
		query = songs_artist[i]
		members = yahoo_search_members(query)
		member = clean_up_members(members)
		query = member + " birthday"
		bday = yahoo_search_bday(query)
		bday = clean_up_birthday(bday)
		if bday != "[]":
			ages.append(int(songs_years[i] - int(bday)))
		else:
			ages.append("BDAY NOT FOUND")
print ages



# yahoo birthplace
# <a class=" fz-4xl fw-s lh-m "
# wikipedia birthplace
# <span class="birthplace">


# wikipedia labels
# <div class="hlist">
