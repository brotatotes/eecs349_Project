import requests, re
from bs4 import BeautifulSoup, SoupStrainer
import parse as p
from textblob import TextBlob
from textstat.textstat import textstat

songs_list = p.parse("./song_titles.csv")
songs_artist = p.parse("./artists.csv")
song_data_headers = ["song", "artist", "word_count", "reading_ease", "polarity", "subjectivity"]
lyric_word_counts = []
lyric_reading_scores = []
sentiments = []

for i in range(0, 5399):
	artist = songs_artist[i].replace(" ","-")
	song = songs_list[i].replace(" ","-")
	query = "http://www.metrolyrics.com/" + song + "-lyrics-" + artist
	print query
	html_doc = requests.get(query)
	page = BeautifulSoup(html_doc.text, 'html.parser')
	verses = page.find_all("div", id="lyrics-body-text")
	if len(verses) > 0:
		lyric = str(verses[0])
		lyric = re.sub(r'\<[^>]*\>', '', lyric)
		lyric = lyric.replace("\n", ".\n")
		lyric_word_counts.append(len(lyric.split()))
		try:
			sentiments.append(TextBlob(lyric).sentiment)
		except:
			sentiments.append(["?", "?"])
		try:
			lyric_reading_scores.append(textstat.flesch_reading_ease(lyric))
		except:
			lyric_reading_scores.append("?")
	else:		
		query = "http://www.songlyrics.com/" +artist + "/" + song +"-lyrics/"
		print query
		html_doc = requests.get(query)
		page = BeautifulSoup(html_doc.text, 'html.parser')
		verses = page.find_all("div", id="songLyricsDiv-outer")
		if len(verses) > 0:
			lyric = str(verses[0])
			lyric = re.sub(r'\<[^>]*\>', '', lyric)
			lyric = lyric.replace("\n", ".\n")
			if lyric[2:19] != "Sorry, we have no":
				try:
					sentiments.append(TextBlob(lyric).sentiment)
				except:
					sentiments.append(["?", "?"])
				try:
					lyric_reading_scores.append(textstat.flesch_reading_ease(lyric))
				except:
					lyric_reading_scores.append("?")
				lyric_word_counts.append(len(lyric.split()))
			else:
				lyric = ""
				print "404"
		else:
			lyric = ""
			print "404"
			sentiments.append(["?", "?"])
print lyric_reading_scores
print sentiments
filename = "lyric_attributes.csv"
file = open(filename, "w")
file.write(",".join(song_data_headers)+"\n")
for i in range(5399):
	file.write(songs_list[i] + "," + songs_artist[i] + "," + str(lyric_word_counts[i]) + "," + str(lyric_reading_scores[i]) + "," +str(sentiments[i][0]) + "," + str(sentiments[i][1]) + "\n")
file.close()