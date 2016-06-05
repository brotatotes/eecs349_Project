import json, requests, pickle
import parse as p

def persistent_request(url):
	"""Function that makes up to 5 api calls and returns the json object"""
	call_attempts = 0
	call_succeeded = False
	while (not call_succeeded) and (call_attempts < 5):
		try:
			r = requests.get(url)
			return r
		except:
			call_attempts += 1
	if r.status_code == 401:
		print "Need new authorization code"
		raise Exception
	print "damn"
	return


def get_top_tags(track_name, artist):
	"""Makes a Last.fm API call and gets the top five song tags for a song in list form"""
	root_url = "http://ws.audioscrobbler.com/2.0/"
	api_key = "2496219e91c3dac719109d2aff2e5919"
	query_string = "?method=track.gettoptags&artist=" + artist + "&track=" + track_name + "&api_key=" + api_key + "&format=json"

	request_url = root_url + query_string

	r = persistent_request(request_url)
	data = json.loads(r.text)
	try:
		return map(lambda x: x["name"], data["toptags"]["tag"][:])
	except:
		[]

with open('grammy_candidates.pickle', 'r') as handle:
		SA = pickle.load(handle)

songs_artist = []
songs_list = []
for i in range(0, len(SA)):
 	songs_list.append(SA[i][0])
 	songs_artist.append(SA[i][1])

song_data_headers = ["song", "artist", "years"]
years = []

genres = ["oldies", "rock", "classic rock", "jazz", "soul", "instrumental", "folk", "country", "pop", "blues", "reggae", "Hip-Hop", "rnb" ,"rap", "indie", "funk", "latin", "electronic", "punk", "Disco"]
song_data_headers = ["song", "artist", "genre"]
lyric_word_counts = []
lyric_reading_scores = []
song_genres = []
for i in range(421):
	artist = songs_artist[i]
	sep = ' Featuring'
	artist = artist.split(sep, 1)[0]	
	data = get_top_tags(songs_list[i], artist)
	if data == None or len(data) == 0:
		print data
		song_genres.append("?")	
	else:
		for j in range(0, len(data)):
			if data[j] in genres:
				song_genres.append(data[j])
				break
			elif j == len(data)-1:
				print data
				song_genres.append("?")
			else:
				continue
	print i
print song_genres
print len(song_genres)

filename = "candidate_genres.csv"
file = open(filename, "w")
file.write(",".join(song_data_headers)+"\n")
for i in range(421):
	file.write(songs_list[i] + "," + songs_artist[i] + "," + song_genres[i] + "\n")
file.close()