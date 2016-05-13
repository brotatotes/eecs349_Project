import json, requests
import parse as p

def persistent_request(url, headers):
	"""Function that makes up to 5 api calls and returns the json object"""
	call_attempts = 0
	call_succeeded = False
	while (not call_succeeded) and (call_attempts < 5):
		try:
			r = requests.get(url, headers=headers)
			return json.loads(r.text)
		except:
			call_attempts += 1

	print "damn"
	return


songs_list = p.parse("./song_titles.csv")
song_years = p.parse("./years.csv")
song_artist = p.parse("./artists.csv")

song_data_headers = ["title", "spotify_id", "artist", "year", "popularity", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]
song_data = []

for i in range(50, 100):
	print (i + 1)
	query = "search?q="+songs_list[i]+"&type=track"
	url = "https://api.spotify.com/v1/"+query
	req_headers = {"Accept": "application/json", "Authorization": "Bearer BQBQI5bM4j0liVDalGA-HyXAKucN9QGW_nUyWOtg_CCawheGb1PGHsmkLPit8cBa2y_p0WpNF-bgGC0UO-uoBbIDYx9ZuZM47dMS9HVl-tUvxn666kCvT80B8Rq0LBk3475lI6wKjUBD87w"}

	data = persistent_request(url, req_headers)
	if not len(data["tracks"]["items"]) == 0:
		#actually getting the attribute's for each instance now
		song_id = data["tracks"]["items"][0]["id"]

		attr_query = "audio-features/" + song_id
		attr_url = "https://api.spotify.com/v1/" + attr_query
		attr_data = persistent_request(attr_url, req_headers)

		pop_query = "tracks/" + song_id + "?market=US"
		pop_url = "https://api.spotify.com/v1/" + pop_query
		pop_data = persistent_request(pop_url, req_headers)

		row = [songs_list[i], song_id, song_artist[i], str(song_years[i])]
		if "popularity" in pop_data.keys():
			row.append(str(pop_data["popularity"]))
		else:
			row.append("?")
		for attribute in song_data_headers[5:]:
			if attribute in attr_data.keys():
				row.append(str(attr_data[attribute]))
			else:
				row.append("?")
		song_data.append(row)

filename = "output.csv"
file = open(filename, "a")
# file.write(",".join(song_data_headers)+"\n")
for song in song_data:
	file.write(",".join(song)+"\n")
file.close()





