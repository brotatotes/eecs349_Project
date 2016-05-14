import requests, json

def get_top_tags(track_name, artist):
	"""Makes a Last.fm API call and gets the top five song tags for a song in list form"""
	root_url = "http://ws.audioscrobbler.com/2.0/"
	api_key = "2496219e91c3dac719109d2aff2e5919"
	query_string = "?method=track.gettoptags&artist=" + artist + "&track=" + track_name + "&api_key=" + api_key + "&format=json"

	request_url = root_url + query_string

	r = requests.get(request_url)

	data = json.loads(r.text)

	return map(lambda x: x["name"], data["toptags"]["tag"][0:5])