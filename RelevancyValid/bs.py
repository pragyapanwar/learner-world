from bs4 import BeautifulSoup
import requests, os
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.snowball import SnowballStemmer

def rem(m):
	stemmer = SnowballStemmer("english")
	tokenizer = RegexpTokenizer(r'\w+')
	l = []
	for i in m:
		l.append(tokenizer.tokenize(str(i).lower()))
	filtered_words = [w for w in l if not w in stopwords.words('english')]
	keywords = []
	for x in filtered_words:
		for y in x:
			keywords.append(stemmer.stem(y))
	return keywords

def relevancy_valid(url):
	r = requests.get(str(url))
	data = r.text
	soup = BeautifulSoup(data,'lxml')
	tags = []
	for tag in soup.find_all('meta'):
		tags.append(tag.get('content'))
		tags.append(tag.get('description'))
	return rem(tags)

## Assuming that desc is our description for the link, here's how we will give the link a score

def score(url, desc):
	keyfound = set(relevancy_valid(url))
	keywords = set(rem(desc))
	# Minimum score = 10%
	i=0
	for x in keywords:
		if x in keyfound:
			i += 1
	if(i==0):
		return 10
	if(i==int(len(keyfound))):
		return 99
	else:
		return (10 + (i/int(len(keyfound)))*100)

## Uncomment the following code to see the score for a particular link!!!!
print (score("https://www.djangoproject.com/download/", [ 'python','Django']))
