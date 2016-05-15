import json, requests
import parse as p
import xmltodict
from textstat.textstat import textstat
songs_without_lyrics = 0
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

song_data_headers = ["song", "artist", "word_count", "reading_ease_scores"]
lyric_word_counts = []
lyric_reading_scores = []
for i in range(0, 5399):
	print (i+1)
	query = "artist=" + songs_artist[i]+ "&song=" + songs_list[i]
	url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?"+query
	data = persistent_request(url)
	if data == None:
		songs_without_lyrics = songs_without_lyrics + 1
		Lyric = None
		lyric_word_counts.append("?")
		lyric_reading_scores.append("?")
		continue
	Lyric = data["GetLyricResult"]['Lyric']
	if Lyric == None:
		songs_without_lyrics = songs_without_lyrics + 1
		Lyric = None
		lyric_word_counts.append("?")
		lyric_reading_scores.append("?")
		continue
	else:
		Lyric = Lyric.replace("\n", ".\n")
		lyric_word_counts.append(len(Lyric.split()))
		try:
			Reading_Ease = textstat.flesch_reading_ease(Lyric)
		except:
			lyric_reading_scores.append("?")
		
		lyric_reading_scores.append(Reading_Ease)

print lyric_reading_scores
print lyric_word_counts

filename = "output.csv"
file = open(filename, "w")
file.write(",".join(song_data_headers)+"\n")
for i in range(5399):
	file.write(songs_list[i] + "," + songs_artist[i] + "," + str(lyric_word_counts[i]) + "," + str(lyric_reading_scores[i]) +"\n")
file.close()