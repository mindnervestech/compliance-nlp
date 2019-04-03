#!/usr/bin/python
# -*- coding: utf-8 -*

from bs4 import BeautifulSoup
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
import spacy
import magic
#find input file encoding
file_d = open('textfile.txt').read()
m = magic.Magic(mime_encoding=True)
encoding = m.from_buffer(file_d)
print encoding

#change file encoding to whatever you want
def get_text(filename):
	import io
	with io.open("textfile.txt", "r", encoding="utf-8") as data_file:
     		contents = data_file.read() 
	revised_content = contents.replace("\n"," ")
	revised_content = revised_content.lower()
	data_file.close()
	return revised_content

def useful_words(data):
	words = nltk.word_tokenize(data)
	stop_words = set(stopwords.words("english"))
	new_wordlist = []
	for word in words:
		if word not in stop_words:
			new_wordlist.append(word)
	return new_wordlist

def remove_punct(data):
	result = [char for char in data if char not in '!#$%&\'()*+,/;<=>?@[\\]^_`{|}~']
	return(''.join(result))

from nltk.stem import PorterStemmer
def stem(data):
	porter = PorterStemmer()
	new_text = porter.stem(data)
	return new_text


def postagging(data):
	tagged_sent = nltk.pos_tag(data)
	propernouns = [word for word,pos in tagged_sent if pos == 'NNP' or 'NNS' or 'NN']
	return propernouns


if __name__ == "__main__":
	text = get_text('textfile.txt')
	#print text
	#clean URLs from string
	urlless_string = re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', text)
	#print urlless_string
	
	clean_text=""
	for i in text:
		clean_text = clean_text+remove_punct(i)
	clean_text=re.sub(' +', ' ',clean_text)	
	clean_text=re.sub('\d.', '',clean_text)
	clean_text=re.sub('\d+', '',clean_text)	#remove numbers
	clean_text = re.sub(r'\b\w\b', ' ', clean_text)	#remove single letters
	print len(clean_text)
	print 'xxx'
	#print clean_text
	new_text = stem(clean_text)	#create word stems
	#print new_text
	words = useful_words(new_text)	#
	#print words
	pos_tagged = postagging(words)
	print(pos_tagged)
	df = pd.DataFrame(data=pos_tagged,columns=['text'])
	#print(df.head())
	#from sklearn.feature_extraction.text import TfidfVectorizer
	#vect = TfidfVectorizer()
	#print vect
	#vect.set_params(ngram_range=(1, 2))
	#vect.set_params(max_df=0.5)
	#v = vect.fit_transform(df['text'])
	#print(v)
