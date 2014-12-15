from nltk import word_tokenize
from collections import defaultdict, Counter
from sys import argv
import random
import operator
import bisect
import string
import re

def make_markov_dict(text, ngram):
	words = word_tokenize(text)
	zippy_words = zip(*[words[i:] for i in xrange(ngram)])
	markov_dict = defaultdict(Counter)
	for t in zippy_words:
		a, b = t[:-1], t[-1]
		markov_dict[a][b] += 1
	return markov_dict

def accumulate(iterable, func=operator.add):
	it = iter(iterable)
	total = next(it)
	yield total
	for el in it:
		total = func(total, el)
		yield total

def choose_word(start_key, freq_dict):
	choices, weights = zip(*freq_dict[start_key].iteritems())
	cumulative_distribution = list(accumulate(weights))
	rando = random.random() * cumulative_distribution[-1]
	return choices[bisect.bisect(cumulative_distribution, rando)] #string

def generate_tweet(markov_dict):
	start_tups = [k for k in markov_dict.keys() if k[0] == '.']
	start_tup = random.choice(start_tups) #let me tell you about my startup
	tweet_length = 0
	tweet_tuples = [start_tup] #list of tuples
	while tweet_length < 90:
		next_word = choose_word(tweet_tuples[-1], markov_dict)
		next_tup = tweet_tuples[-1][1:] + (next_word,)
		tweet_length += len(next_word) + 1
		tweet_tuples.append(next_tup)
	last_tup = tweet_tuples[-1]
	for i in xrange(4): #try four times to get a good end of tweet
		if '.' in markov_dict[last_tup].values():
			tweet_tuples.append(('.',))
			return tup_to_tweet(tweet_tuples) #RENAME
		else:
			last_word = choose_word(last_tup, markov_dict)
			last_tup = last_tup[1:] + (last_word,)
			continue
	tweet_tuples.append(('.',))
	return tup_to_tweet(tweet_tuples)

def tup_to_tweet(tuple_list):
	word_list = [x[0] for x in tuple_list[1:-1]] + list(tuple_list[-1])
	tweet = ''
	for i in word_list:
		if i not in string.punctuation:
			tweet += i + ' '
		else:
			tweet = tweet.strip() + i + ' '
	#almost = tweet.strip() #TODO MAKE AN RE TO GET RID OF PUNC!!
	return tweet.strip()

if __name__ == '__main__':
	with open(sys.arv[1]) as f:
		my_markov = make_markov_dict(f.read())
	print generate_tweet(my_markov)
