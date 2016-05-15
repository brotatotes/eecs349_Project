import requests, re, os
from bs4 import BeautifulSoup, SoupStrainer
import parse as p
from textblob import TextBlob
from textstat.textstat import textstat

def persistent_request(url):
	"""Function that makes up to 5 api calls and returns the json object"""
	call_attempts = 0
	call_succeeded = False
	while (not call_succeeded) and (call_attempts < 5):
		try:
			html_doc = requests.get(url)
			return html_doc
		except:
			call_attempts += 1
	if html_doc.status_code == 401:
		print "Need new authorization code"
		raise Exception
	print "damn"
	return

songs_list = p.parse("./song_titles.csv")
songs_artist = p.parse("./artists.csv")
song_data_headers = ["song", "artist", "word_count", "reading_ease", "polarity", "subjectivity"]
lyric_word_counts = []
lyric_reading_scores = []
sentiments = []

for i in range(0, 5399):
	artist = songs_artist[i].replace(" ","-")
	song = songs_list[i].replace(" ","-")
	url = "http://www.metrolyrics.com/" + song + "-lyrics-" + artist
	print url
	html_doc = persistent_request(url)
	page = BeautifulSoup(html_doc.text, 'html.parser')	
	verses = page.find_all("div", id="lyrics-body-text")
	if len(verses) > 0:
		lyric = str(verses[0])
		lyric = re.sub(r'\<[^>]*\>', '', lyric)
		lyric = re.sub("\n\s*\n*", "\n", lyric)
		lyric = lyric.replace("\n", ".\n")
		try:
			sentiments.append(TextBlob(lyric).sentiment)
		except:
			sentiments.append(["?", "?"])
		try:
			lyric_reading_scores.append(textstat.flesch_reading_ease(lyric))
		except:
			lyric_reading_scores.append("?")
		print lyric
	else:		
		url = "http://www.songlyrics.com/" +artist + "/" + song +"-lyrics/"
		print url
		html_doc = persistent_request(url)
		page = BeautifulSoup(html_doc.text, 'html.parser')
		verses = page.find_all("div", id="songLyricsDiv-outer")
		if len(verses) > 0:
			lyric = str(verses[0])
			lyric = re.sub(r'\<[^>]*\>', '', lyric)
			lyric = re.sub("\n\s*\n*", "\n", lyric)
			lyric = lyric.replace("\n", ".\n")
			if "Sorry, we have no" not in lyric:
				try:
					sentiments.append(TextBlob(lyric).sentiment)
				except:
					sentiments.append(["?", "?"])
				try:
					lyric_reading_scores.append(textstat.flesch_reading_ease(lyric))
				except:
					lyric_reading_scores.append("?")
				lyric_word_counts.append(len(lyric.split()))
				print lyric
			else:
				lyric = ""
				print "404"
		else:
			lyric = ""
			print "404"
			sentiments.append(["?", "?"])
			
filename = "lyric_attributes.csv"
file = open(filename, "w")
file.write(",".join(song_data_headers)+"\n")
for i in range(5399):
	file.write(songs_list[i] + "," + songs_artist[i] + "," + str(lyric_word_counts[i]) + "," + str(lyric_reading_scores[i]) + "," +str(sentiments[i][0]) + "," + str(sentiments[i][1]) + "\n")
file.close()