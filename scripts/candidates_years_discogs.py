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

with open('grammy_candidates.pickle', 'r') as handle:
		SA = pickle.load(handle)

songs_artist = []
songs_list = []
for i in range(0, len(SA)):
 	songs_list.append(SA[i][0])
 	songs_artist.append(SA[i][1])

song_data_headers = ["song", "artist", "years"]
years = []

for i in range(len(songs_artist)):
	artist = songs_artist[i]
	sep = ' Featuring'
	artist = artist.split(sep, 1)[0]	

	url = "https://api.discogs.com/database/search?release_title=" +str(songs_list[i])+"&artist="+artist+"&token=wijuIjjAhxEdvPVotElLdycDEosgTyAKkVdiigVD"
	print url
	data = persistent_request(url)
	try:
		if len(data["results"]) > 0:
			try:
				year = data["results"][0]["year"]
				years.append(year)
			except:
				years.append("?")
		else:
			years.append("?")
	except:
		years.append("?")
print years


filename = "candidate_years.csv"
file = open(filename, "w")
file.write(",".join(song_data_headers)+"\n")
for i in range(len(songs_artist)):
	try:
		file.write(str(songs_list[i]) + "," + str(songs_artist[i]) + "," + str(years[i]) + "\n")
	except:
		file.write(str(songs_list[i]) + "," + str(songs_artist[i]) + ",?" + "\n")
file.close()