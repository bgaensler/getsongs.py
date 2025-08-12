#!/usr/bin/python3.8

# Code to automatically list last 10 songs on last.fm
# Written by BMG, 21jul2024

outpath = '/path-to-file/lastfm.inc'

import re, requests, json, time, codecs, pandas as pd
from better_profanity import profanity
key ='LAST.FM API KEY'
username = 'USERNAME'

# Load words from the better_profanity database
profanity.load_censor_words()
curse_words = set(str(word) for word in profanity.CENSOR_WORDSET) # set of all loaded curse words

def star_vowels(word):
    return re.sub(r'[aeiouAEIOU]', '*', word)

def censor_substrings_with_better_profanity(text, curse_words):
    result = text
    for badword in curse_words:
        # Compile a case-insensitive pattern for the word as a substring
        pattern = re.compile(re.escape(badword), re.IGNORECASE)
        def repl(match):
            return star_vowels(match.group(0))
        result = pattern.sub(repl, result)
    return result

# how long to pause between consecutive API requests
pause_duration = 0.2

url = 'https://ws.audioscrobbler.com/2.0/?method=user.get{}&user={}&api_key={}&limit={}&extended={}&page={}&format=json'
limit = 10 #api lets you retrieve up to 200 records per call
extended = 0 #api lets you retrieve extended data for each track, 0=no, 1=yes
page = 1 #page of results to start retrieving at

method = 'recenttracks'
request_url = url.format(method, username, key, limit, extended, page)
response = requests.get(request_url).json()
lastlisten = response[method]['track'][0]['date']['#text'][0:11]

f = codecs.open(outpath,'w','utf-8')

f.write('<ul>'+'\n')
f.write('<li> <a href=\"http://www.last.fm/user/bgaensler/?chartstyle=iTunesFIXED\">What I\'m listening to</a> (last listen '+lastlisten+'):'+'\n')
f.write('<ul class=bullets>'+'\n')
for x in range(10):
	f.write("<li> "+censor_substrings_with_better_profanity(response[method]['track'][x]['name'],curse_words)+" - "+censor_substrings_with_better_profanity(response[method]['track'][x]['artist']['#text'],curse_words)+"\n")
f.write('</ul>'+"\n")
