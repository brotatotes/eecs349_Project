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

	if r.status_code == 401:
		print "Need new authorization code"
		raise Exception
	print "damn"
	return

def add_songs(range_begin, range_end):
	songs_list = p.parse("./song_titles.csv")
	song_years = p.parse("./years.csv")
	song_artist = p.parse("./artists.csv")

	song_data_headers = ["title", "spotify_id", "artist", "year", "popularity", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]
	song_data = []

	for i in range(range_begin, range_end):
		print (i + 1)
		query = "search?q="+songs_list[i]+ " " + song_artist[i] +"&type=track"
		url = "https://api.spotify.com/v1/"+query
		req_headers = {"Accept": "application/json", "Authorization": "Bearer BQBnzJZWXmlfH3dZ1qugmisod_JuLniew6rP_CqitAxvuEa0eSm_7U7ikRk2cQoi2hypyXFhKEUFZyW78UAffYsRUgh8fudYn_3MP3sjUjgnauPqn_8r5dURfa0wlBCJuZGXkxeazQxTjL8"}

		data = persistent_request(url, req_headers)
		if data == None:
			continue
		elif not "tracks" in data.keys():
			continue
		elif not len(data["tracks"]["items"]) == 0:
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
			print row
			song_data.append(row)

	filename = "output.csv"
	file = open(filename, "a")
	# file.write(",".join(song_data_headers)+"\n")
	for song in song_data:
		file.write(",".join(song)+"\n")
	file.close()



range_start = 0
range_end = 1
while range_end <= 1:
	add_songs(range_start, range_end)
	print "songs added from " + str(range_start) + " to " + str(range_end)
	range_start += 100
	range_end += 100





