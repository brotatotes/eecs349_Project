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
	followers = []	

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
		artist = song_artist[i]
		sep = ' Featuring'
		artist = artist.split(sep, 1)[0]
		query = "search?q="+ artist +"&type=artist"
		url = "https://api.spotify.com/v1/"+query
		req_headers = {"Accept": "application/json", "Authorization": "Bearer BQBXDYdUuQUQaC1GvbCXx4LY5kV-wTFvVhe84imLN-VDwDRTO1L3obyNEw-K1komwPxEMS6YBXISDKaaak6vchoUKRLaYfZ1hZvYewEBnqSn6-NlAYH3Ww_u3DtIXHguQA9ZV5fwujeVangacJmWXk1P9Ll6E_Q"}

		data = persistent_request(url, req_headers)
		if data == None:
			followers.append("?")
		elif not "artists" in data.keys():
			followers.append("?")
		elif not len(data["artists"]["items"]) == 0:
			#actually getting the attribute's for each instance now
			followers.append(data["artists"]["items"][0]["followers"]["total"])
		else:
			followers.append("?")
	print followers
	filename = "candidate_artist_popularity.csv"
	file = open(filename, "w")
	for i in range(0, range_end):
		if followers[i] != None:
			file.write(songs_list[i] + "," + song_artist[i] + "," + str(followers[i]) + "\n")
		else:
			file.write(songs_list[i] + "," + song_artist[i] + "," + "?" + "\n")

	file.close()

add_songs(0, 421)






