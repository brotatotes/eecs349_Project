import requests, re, os, pickle
from bs4 import BeautifulSoup, SoupStrainer
import parse as p
from textblob import TextBlob
from textstat.textstat import textstat

def persistent_request(url):
	"""Function that makes up to 10 api calls and returns the json object"""
	call_attempts = 0
	call_succeeded = False
	while (not call_succeeded) and (call_attempts < 10):
		try:
			html_doc = requests.get(url)
			return html_doc
		except:
			call_attempts += 1
	print "damn"
	return

def add_lyric_data(range_start, range_end, restart=False):

	with open('grammy_candidates.pickle', 'r') as handle:
  		SA = pickle.load(handle)

	songs_artist = []
	songs_list = []
	for i in range(0, len(SA)):
	 	songs_list.append(SA[i][0])
	 	songs_artist.append(SA[i][1])

	song_data_headers = ["song", "artist", "word_count", "reading_ease", "polarity", "subjectivity"]
	lyric_word_counts = []
	lyric_reading_scores = []
	sentiments = []

	for i in range(range_start, range_end):
		print (i+1)
		artist = songs_artist[i].replace(" ","-")
		song = songs_list[i].replace(" ","-")
		url = "http://www.metrolyrics.com/" + song + "-lyrics-" + artist
		# print url
		html_doc = persistent_request(url)

		if html_doc == None:
			lyric_word_counts.append("?")
			lyric_reading_scores.append("?")
			sentiments.append(["?", "?"])
			print songs_list[i] + "," + songs_artist[i] + "," + str(lyric_word_counts[i - range_start]) + "," + str(lyric_reading_scores[i - range_start]) + "," +str(sentiments[i - range_start][0]) + "," + str(sentiments[i - range_start][1])
			continue

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
			lyric_word_counts.append(len(lyric.split()))
			# print lyric
		else:		
			url = "http://www.songlyrics.com/" +artist + "/" + song +"-lyrics/"
			# print url
			html_doc = persistent_request(url)


			if html_doc == None:
				lyric_word_counts.append("?")
				lyric_reading_scores.append("?")
				sentiments.append(["?", "?"])
				print songs_list[i] + "," + songs_artist[i] + "," + str(lyric_word_counts[i - range_start]) + "," + str(lyric_reading_scores[i - range_start]) + "," +str(sentiments[i - range_start][0]) + "," + str(sentiments[i - range_start][1])
				continue

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
					# print lyric
				else:
					lyric = ""
					lyric_word_counts.append("?")
					lyric_reading_scores.append("?")
					sentiments.append(["?", "?"])
					# print "404"
			else:
				lyric = ""
				# print "404"
				lyric_word_counts.append("?")
				lyric_reading_scores.append("?")
				sentiments.append(["?", "?"])
		print songs_list[i] + "," + songs_artist[i] + "," + str(lyric_word_counts[i - range_start]) + "," + str(lyric_reading_scores[i - range_start]) + "," +str(sentiments[i - range_start][0]) + "," + str(sentiments[i - range_start][1])
				
	filename = "candidates_lyric_attributes.csv"
	
	if restart:
		file = open(filename, "w")
		file.write(",".join(song_data_headers)+"\n")
	else:
		file = open(filename, "a")

	for i in range(len(lyric_word_counts)):
		row = songs_list[range_start + i] + "," + songs_artist[range_start + i] + "," + str(lyric_word_counts[i]) + "," + str(lyric_reading_scores[i]) + "," +str(sentiments[i][0]) + "," + str(sentiments[i][1]) + "\n"
		file.write(row)
	file.close()



# add_lyric_data(0, 100, restart=True)

add_lyric_data(0, 421)