import json, requests
import parse as p
import xmltodict
# obj = untangle.parse('path/to/file.xml')
def persistent_request(url):
	"""Function that makes up to 5 api calls and returns the json object"""
	call_attempts = 0
	call_succeeded = False
	while (not call_succeeded) and (call_attempts < 5):
		try:
			r = requests.get(url)
			doc = xmltodict.parse(r.content)
			return doc
		except:
			call_attempts += 1

	if r.status_code == 401:
		print "Need new authorization code"
		raise Exception
	print "damn"
	return

songs_list = p.parse("./song_titles.csv")
songs_artist = p.parse("./artists.csv")

song_data_headers = ["song", "artist", "lyrics"]
song_data = []
for i in range(0, len(songs_list)):
	print (i + 1)
	query = "artist=" + songs_artist[i]+ "&song=" + songs_list[i]
	url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?"+query
	data = persistent_request(url)
	print data["GetLyricResult"]['Lyric']
	# print data.root()

	# if data == None:
	# 	continue
	# elif not "tracks" in data.keys():
	# 	continue
	# elif not len(data["tracks"]["items"]) == 0:
	# 	#actually getting the attribute's for each instance now
	# 	song_id = data["tracks"]["items"][0]["id"]

	# 	attr_query = "audio-features/" + song_id
	# 	attr_url = "https://api.spotify.com/v1/" + attr_query
	# 	attr_data = persistent_request(attr_url, req_headers)

	# 	pop_query = "tracks/" + song_id + "?market=US"
	# 	pop_url = "https://api.spotify.com/v1/" + pop_query
	# 	pop_data = persistent_request(pop_url, req_headers)

	# 	row = [songs_list[i], song_id, song_artist[i], str(song_years[i])]
