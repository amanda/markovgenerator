from nltk import word_tokenize
from collections import defaultdict, Counter
from sys import argv
import random
import operator
import bisect
import string
import re


class MarkovGenerator(object):

    '''class for making markov-generated text output of a 
    user-supplied length based on the supplied source text'''

    def __init__(self, text, length, ngram=2):
        self.text = text
        self.ngram = ngram
        self.length = length
        self.markov_dict = self.make_markov_dict()

    def make_markov_dict(self):
        '''returns a dict of {ngram tuple: Counter} 
        counting the number of times words follow an ngram'''
        text = self.text
        ngram = self.ngram
        words = word_tokenize(text)
        zippy_words = zip(*[words[i:] for i in xrange(ngram + 1)])
        markov_dict = defaultdict(Counter)
        for t in zippy_words:
            a, b = t[:-1], t[-1]
            markov_dict[a][b] += 1
        return markov_dict

    def choose_word(self, start_key):
        '''picks a word to follow an ngram
        based on frequency using an accumulate func'''
        def accumulate(iterable, func=operator.add):
            it = iter(iterable)
            total = next(it)
            yield total
            for el in it:
                total = func(total, el)
                yield total
        choices, weights = zip(*self.markov_dict[start_key].iteritems())
        cumulative_distribution = list(accumulate(weights))
        rando = random.random() * cumulative_distribution[-1]
        return choices[bisect.bisect(cumulative_distribution, rando)]

    def ngrams_to_words(tuple_list):
        '''(list of ngram tuples) -> str
        turns the tuples into a readable sentence'''
        word_list = [x[0] for x in tuple_list[1:-1]] + list(tuple_list[-1])
        words = ''
        for i in word_list:
            if i not in string.punctuation:
                words += i + ' '
            else:
                words = words.strip() + i + ' '
        return words.strip()

    def generate_words(self):
        '''generates new text'''
        start_tups = [k for k in self.markov_dict.keys() if k[-1] == '.']
        # let me tell you about my startup
        start_tup = random.choice(start_tups)
        words_length = 0
        words_tuples = [start_tup]
        while words_length < self.length:
            next_word = self.choose_word(words_tuples[-1])
            next_tup = words_tuples[-1][1:] + (next_word,)
            words_length += len(next_word) + 1
            words_tuples.append(next_tup)
        last_tup = words_tuples[-1]
        for i in xrange(4):  # try four times to get a good end of sentence
            if '.' in self.markov_dict[last_tup].values():
                words_tuples.append(('.',))
                self.generated_text = tup_to_words(words_tuples)
            else:
                last_word = self.choose_word(last_tup)
                last_tup = last_tup[1:] + (last_word,)
                continue
        words_tuples.append(('.',))
        self.generated_text = ngrams_to_words(words_tuples)
        if self.generated_text[-2] in string.punctuation:
            self.generated_text = self.generated_text[:-2] + '.'
        return self.generated_text
