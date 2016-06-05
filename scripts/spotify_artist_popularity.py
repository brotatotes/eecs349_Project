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

	songs_list = p.parse("../data/song_titles.csv")
	song_artist = p.parse("../data/artists.csv")

	song_data_headers = ["title", "spotify_id", "artist", "popularity", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]
	song_data = []

	for i in range(range_begin, range_end):
		print (i + 1)
		artist = song_artist[i]
		sep = ' Featuring'
		artist = artist.split(sep, 1)[0]

		query = "search?q="+ artist +"&type=artist"
		url = "https://api.spotify.com/v1/"+query
		req_headers = {"Accept": "application/json", "Authorization": "Bearer BQBU_HrkpxMZ0b_YAwKjc3YUf6bJi4Rykyx-RsXpAbhEjLkud9qY3OInWvSOD9hDTmq4YlEYf9ZLzI5M5AgtP5dSO2L-aiUwAy20YHBK3NdQaPPDk72-akUFzlQ5PxbgyEIHoFbxE5lr0aR6vdv9vzQKxx88zGU"}

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
	filename = "artist_popularity.csv"
	file = open(filename, "w")
	for i in range(0, range_end):
		if followers[i] != None:
			file.write(songs_list[i] + "," + song_artist[i] + "," + str(followers[i]) + "\n")
		else:
			file.write(songs_list[i] + "," + song_artist[i] + "," + "?" + "\n")

	file.close()

add_songs(0, 5399)






