# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 14:57:01 2017

@author: Lynn
"""

import json
from urllib.request import urlopen

url = urlopen("http://kevincrook.com/utd/tweets.json")
input_file = json.load(url)

language = []
text = []
for i in range(len(input_file)):
    file = input_file[i]
    if 'text' in file:
        string = json.dumps(file['text'], sort_keys = True, indent = 4)
        text.append(string)
    if 'lang' in file:
        language.append(file['lang'])

langcnt = [[x,language.count(x)] for x in set(language)]
langcnt_final = sorted(langcnt, key=lambda langcnt: langcnt[1], reverse=True)
for i in range(len(langcnt)):
    langcnt[i][0] = langcnt[i][0][:2]
    langcnt[i][1] = str(langcnt[i][1])
langcnt_final.insert(0, str(len(input_file)))
langcnt_final.insert(1, str(len(text)))

with open("twitter_analytics.txt", "w") as f:
    for elem in langcnt_final:
        if type(elem) == str:
            f.write(elem + '\n')
        else:
            f.write('{},{}\n'.format(*elem))

with open("tweets.txt", "w") as f:
    for elem in text:
        f.write(elem + '\n')
