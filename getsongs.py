#!/usr/bin/python3.8

# Code to automatically list last 10 songs on last.fm
# Written by BMG, 21jul2024

outpath = '/path-to-file/lastfm.inc'

import requests, json, time, codecs, pandas as pd
key ='LAST FM API KEY'
username = 'USERNAME'

# how long to pause between consecutive API requests
pause_duration = 0.2

url = 'https://ws.audioscrobbler.com/2.0/?method=user.get{}&user={}&api_key={}&limit={}&extended={}&page={}&format=json'
limit = 10 #api lets you retrieve up to 200 records per call
extended = 0 #api lets you retrieve extended data for each track, 0=no, 1=yes
page = 1 #page of results to start retrieving at

method = 'recenttracks'
request_url = url.format(method, username, key, limit, extended, page)
response = requests.get(request_url).json()

f = codecs.open(outpath,'w','utf-8')

f.write('<ul>'+'\n')
for x in range(10):
	f.write("<li> "+response[method]['track'][x]['name']+" - "+response[method]['track'][x]['artist']['#text']+"\n")    
f.write('</ul>'+"\n")

