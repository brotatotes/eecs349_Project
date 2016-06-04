import requests, re, os
import pickle
from bs4 import BeautifulSoup, SoupStrainer

S = []
A = []
urllist = ["http://www.billboard.com/charts/hot-100/2016-05-21", "http://www.billboard.com/charts/hot-100/2016-05-21"]

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


def remove_duplicates(L):
    seen = set()
    seen_add = seen.add
    return [x for x in L if not (x in seen or seen_add(x))]

def billboard(url):
	html_doc = persistent_request(url)
	soup = BeautifulSoup(html_doc.text, 'html.parser')

	songs = soup.find_all('h2', {'class' : "chart-row__song"})
	for i in range(0, len(songs)):
		songs[i] = str(songs[i]).replace('<h2 class="chart-row__song">', '')
		songs[i] = str(songs[i]).replace('</h2>', '')
		if '&amp;' in songs[i]:
			songs[i] = str(songs[i]).replace('&amp;', '&')

	artists = soup.find_all('a', {'class' : "chart-row__artist"})
	for i in range(0, len(artists)):
		artists[i] = re.sub(r'\<[^>]*\>', '', str(artists[i]))
		artists[i] = artists[i].strip()
		if '&amp;' in artists[i]:
			artists[i] = str(artists[i]).replace('&amp;', '&')
	return songs, artists

for i in range(0, len(urllist)):
	mysongs, myartists = billboard("http://www.billboard.com/charts/hot-100/2016-05-21")
	S.append(mysongs)
	A.append(myartists)

S = [item for sublist in S for item in sublist]
A = [item for sublist in A for item in sublist]
SA = []
for i in range(0, len(S)):
	SA.append((S[i], A[i]))
SA = set(SA)

with open('grammy_candidates.pickle', 'wb') as handle:
  pickle.dump(SA, handle)


filename = "../data/59th_grammy_song_candidates.csv"
file = open(filename, "w")
for i in range(0, len(S)):
	file.write(S[i] + "," + A[i] + "\n")
file.close()
