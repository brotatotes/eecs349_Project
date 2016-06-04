import requests, re, os
import pickle
from bs4 import BeautifulSoup, SoupStrainer

S = []
A = []
urllist = ["2016-06-11","2016-06-04","2016-05-28","2016-05-21","2016-05-14","2016-05-07","2016-04-30","2016-04-23","2016-04-16","2016-04-09","2016-04-02","2016-03-26","2016-03-19","2016-03-12","2016-03-05","2016-02-27","2016-02-20","2016-02-13","2016-02-06","2016-01-30","2016-01-23","2016-01-16","2016-01-09","2016-01-02","2015-12-26","2015-12-19","2015-12-12","2015-12-05","2015-11-28","2015-11-21","2015-11-14","2015-11-07","2015-10-31","2015-10-24","2015-10-17","2015-10-10","2015-10-03"]
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
	print len(artists)
	for i in range(0, len(artists)):
		artists[i] = re.sub(r'\<[^>]*\>', '', str(artists[i]))
		artists[i] = artists[i].strip()
		if '&amp;' in artists[i]:
			artists[i] = str(artists[i]).replace('&amp;', '&')
	return songs, artists

for i in range(0, len(urllist)):
	print i
	mysongs, myartists = billboard("http://www.billboard.com/charts/hot-100/" + urllist[i])
	if i == 12:
		myartists.insert(11, "Fifth Harmony Featuring Ty Dolla $ign")
		myartists.insert(78, "Flo Rida Featuring Jason Derulo")
		print myartists
	elif i ==13:
		myartists.insert(95, "Desiigner")
		print myartists
	S.append(mysongs)
	A.append(myartists)
S = [item for sublist in S for item in sublist]
A = [item for sublist in A for item in sublist]
SA = []
for i in range(0, len(S)):
	SA.append((S[i], A[i]))
SA = list(set(SA))

with open('grammy_candidates.pickle', 'wb') as handle:
  pickle.dump(SA, handle)

print SA
filename = "../data/59th_grammy_song_candidates.csv"
file = open(filename, "w")
for i in range(0, len(SA)):
	file.write('"' + SA[i][0] + '"' + "," + '"' + SA[i][1] + '"' + "\n")
file.close()
