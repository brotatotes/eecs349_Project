import requests, re, os, json
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


songs_years = p.parse("../data/years.csv")
songs_artist = p.parse("../data/artists.csv")
songs_list = p.parse("../data/song_titles.csv")
song_data_headers = ["song", "artist", "labels"]
labels = []

for i in range(5399):
	url = "https://api.discogs.com/database/search?release_title=" +str(songs_list[i])+"&artist="+ str(songs_artist[i])+"&token=wijuIjjAhxEdvPVotElLdycDEosgTyAKkVdiigVD"
	print url
	data = persistent_request(url)
	if len(data["results"]) > 0:
		label = data["results"][0]["label"]
		labels.append(label[0])
	else:
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