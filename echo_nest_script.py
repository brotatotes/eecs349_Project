import json, requests
import parse as p

songs_list = p.parse("./song_titles.csv")
song_years = p.parse("./years.csv")
song_artist = p.parse("./artists.csv")

song_data_headers = ["title", "spotify_id", "artist", "year", "popularity", "danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness", "instrumentalness", "liveness", "valence", "tempo", "duration_ms", "time_signature"]
song_data = []

for i in range(0, len(songs_list)):
	query = "search?q="+songs_list[i]+"&type=track"
	url = "https://api.spotify.com/v1/"+query
	req_headers = {"Accept": "application/json", "Authorization": "Bearer BQDGsRqClkWXzONAQlvT_a-ronXTOmoEWTQNIBXOugjtNJZNHnkNrQC4lqB4qj_RHInYHZCVe8sLaKGAVe-vQAguODtiO9Gt8SwTb37uwj_UNVCmBeh6R8l-Ads22Uiq4ewRRJUq8FuKJZU"}

	r = requests.get(url,headers=req_headers)
	print i, songs_list[i]
	data = json.loads(r.text)
	if not len(data["tracks"]["items"]) == 0:
		#actually getting the attribute's for each instance now
		song_id = data["tracks"]["items"][0]["id"]

		attr_query = "audio-features/" + song_id
		attr_url = "https://api.spotify.com/v1/" + attr_query
		r2 = requests.get(attr_url, headers=req_headers)
		attr_data = json.loads(r2.text)

		pop_query = "tracks/" + song_id + "?market=US"
		pop_url = "https://api.spotify.com/v1/" + pop_query
		r3 = requests.get(pop_url, headers=req_headers)
		pop_data = json.loads(r3.text)
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
file = open(filename, "w")
file.write(",".join(song_data_headers)+"\n")
for song in song_data:
	file.write(",".join(song)+"\n")
file.close()





