import json, requests, pickle
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

	# if r.status_code == 401:
	# 	print "Need new authorization code"
	# 	raise Exception
	print "damn"
	return

def add_songs(range_begin, range_end):
	with open('grammy_candidates.pickle', 'r') as handle:
		SA = pickle.load(handle)

	song_artist = []
	songs_list = []
	for i in range(0, len(SA)):
	 	songs_list.append(SA[i][0])
	 	song_artist.append(SA[i][1])


	song_data_headers = ["title", "spotify_id", "artist", "popularity", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]
	song_data = []

	for i in range(range_begin, range_end):
		print (i + 1)
		query = "search?q="+songs_list[i]+ " " + song_artist[i] +"&type=track"
		url = "https://api.spotify.com/v1/"+query
		req_headers = {"Accept": "application/json", "Authorization": "Bearer BQB3cM6s9PWKyVfxcySw_zgKKR3JEh0BHmYMpMBdtjxtdB5NxOZXX3ghaTpzCFvCJE3b-Ha5nIv6limuWcp4j5VkcTa-MPn9tlHi53rWt6NmWNpucFToIOtvvSBhSdhcP8071JXCBBvzlEp-haM0GmELwj6lSGc"}

		data = persistent_request(url, req_headers)
		if data == None:
			song_data.append([songs_list[i], '?', song_artist[i],'?', '?','?', '?','?', '?','?', '?','?', '?','?', '?','?', '?'])
		elif not "tracks" in data.keys():
			song_data.append([songs_list[i], '?', song_artist[i],'?', '?','?', '?','?', '?','?', '?','?', '?','?', '?','?', '?'])
		elif not len(data["tracks"]["items"]) == 0:
			#actually getting the attribute's for each instance now
			song_id = data["tracks"]["items"][0]["id"]

			attr_query = "audio-features/" + song_id
			attr_url = "https://api.spotify.com/v1/" + attr_query
			attr_data = persistent_request(attr_url, req_headers)

			pop_query = "tracks/" + song_id + "?market=US"
			pop_url = "https://api.spotify.com/v1/" + pop_query
			pop_data = persistent_request(pop_url, req_headers)

			row = [songs_list[i], song_id, song_artist[i]]



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
		else:
			song_data.append([songs_list[i], '?', song_artist[i],'?', '?','?', '?','?', '?','?', '?','?', '?','?', '?','?', '?'])

	print song_data
	filename = "candidate_echo_nest.csv"
	file = open(filename, "w")
	file.write(",".join(song_data_headers)+"\n")
	for song in song_data:
		file.write(",".join(song)+"\n")
	file.close()



add_songs(0, 421)






