import requests, re, os
import pickle
import time

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

with open("grammy_candidates.pickle","rb") as handle:
	sa = pickle.load(handle)

query = []
for song in sa:
	songname = song[0]
	artistname = song[1]
	songname = songname.replace(" ","+")
	songname = songname.replace(",","")
	artistname = artistname.replace(" ","+")
	artistname = artistname.replace(",","")
	query.append(songname+"+"+artistname+"+released")


i = 0
years = []
for q in query:
	marker = '<span class="_m3b">'
	# time.sleep(0.1)
	r = persistent_request("https://www.google.com/search?q="+q).text
	place = r.find(marker)
	if place != -1:
		print str(i)+": "+r[place+len(marker):place+len(marker)+4]
		years.append(r[place+len(marker):place+len(marker)+4])
	else:
		print str(i)+": ?"
		years.append("?")
	i += 1

with open("years.csv","w") as writefile:
	for y in years:
		writefile.write(y+"\n")


