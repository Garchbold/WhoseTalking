#!/usr/bin/python

#-----------------------------------------------------------------------
# twitter-authorize:
#  - step through the process of creating and authorization a
#    Twitter application.
#-----------------------------------------------------------------------

import tweepy
import time
import json
import sys
import fileinput
import re
import cgi
import urllib2

data = json.load(urllib2.urlopen('https://boiling-inferno-993.firebaseio.com/hashtag.json'))

form = cgi.FieldStorage()
searchterm = form.getvalue('searchbox')

auth = tweepy.OAuthHandler("EKbYg6CUbKQRvVqfr0mVgbFq6", "qG9hnE8HtzbLBxBeynUEaWLdZdEt6pIGaZJLNiDIa21wz2ngd5")
auth.set_access_token("703518623701164032-zOf5QwEgVFmV58QW67qqqbojwYWDGan", "bumLD5Vq1uaBi55Uv47vKFLRmJvtYj6i0NgfFmxgfHmIe")

api = tweepy.API(auth)

word_counts = {}
PRINT_FREQUENCY = 5
MIN_WORD_LENGTH = 3
PUNCTUATION = [".", ",", "/", "#", "@", "(", ")"]
most_popular = []

def print_word_counts():
	ordered_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

	f = open("/Users/George/documents/WhoseTalking/WTwebsite/files.txt", 'w')
        for word,count in ordered_word_counts[:20]:
            word = word.encode('utf-8')
            #print count, "\t", word
            f.write(str(count) + "\t" + word + "\n")
	f.close()
	
#livestream
class MyStreamListener(tweepy.StreamListener):
	def on_status(self, tweet):
		description = tweet.user.description or ''

		for separator in PUNCTUATION:	
			description = description.replace(separator, " ")
		
		words = description.lower().split()

		for word in words:
			if len(word) > MIN_WORD_LENGTH:
				if word in word_counts:
					word_counts[word] += 1
				else:
					word_counts[word] = 1

		print_word_counts() 



myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())

myStream.filter(track=[data])





