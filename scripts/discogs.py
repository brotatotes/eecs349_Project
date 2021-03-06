import requests, re, os, json, pickle
from bs4 import BeautifulSoup, SoupStrainer
import parse as p

def persistent_request(url):
	"""Function that makes up to 5 api calls and returns the json object"""
	call_attempts = 0
	call_succeeded = False
	while (not call_succeeded) and (call_attempts < 5):
		try:
			r = requests.get(url)
			return json.loads(r.content)
		except:
			call_attempts += 1

	# if r.status_code == 401:
	# 	print "Need new authorization code"
	# 	raise Exception
	print "damn"
	return

songs_list = p.parse("../data/song_titles.csv")
songs_artist = p.parse("../data/artists.csv")

song_data_headers = ["song", "artist", "labels"]
labels = []

for i in range(5399):
	artist = songs_artist[i]
	sep = ' Featuring'
	artist = artist.split(sep, 1)[0]	
	sep = ' feat'
	artist = artist.split(sep, 1)[0]	
	url = "https://api.discogs.com/database/search?release_title=" +str(songs_list[i])+"&artist="+artist+"&token=wijuIjjAhxEdvPVotElLdycDEosgTyAKkVdiigVD"
	print url
	data = persistent_request(url)
	try:
		if len(data["results"]) > 0:
			try:
				print data["results"][0]["label"]
				labels.append(data["results"][0]["label"][0])
			except:
				labels.append("?")
		else:
			labels.append("?")
	except:
		labels.append("?")
print labels


filename = "labels.csv"
file = open(filename, "w")
file.write(",".join(song_data_headers)+"\n")
for i in range(5399):
	try:
		file.write(str(songs_list[i]) + "," + str(songs_artist[i]) + "," + str(labels[i]) + "\n")
	except:
		file.write(str(songs_list[i]) + "," + str(songs_artist[i]) + ",?" + "\n")
file.close()