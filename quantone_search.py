import requests

query = "albums?title=rumours"
new_query = raw_input('Enter a query: ')
if not new_query == '':
	query = new_query
url = "https://data.quantonemusic.com/v3/"+query
req_headers = {"Host": "data.quantonemusic.com", "Connection":"keep-alive", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Encoding":"gzip,deflate,sdch", "Accept-Language": "en-GB,en-US;q=0.8,en;q=0.6", "Accept-Charset":"ISO-8859-1,utf-8;q=0.7,*;q=0.3","AppID":"b8ff991d", "AppKey":"c4a836eda8cdc7ec6a7462c3c1e1b523"}


r = requests.get(url,headers=req_headers)
print r.url