"""Markov chain implementation supporting arbitrary n-gram length."""
import sys
import string
import re
import random
import operator
from collections import defaultdict, Counter
import bisect
import nltk


#if sys.version_info > (2, 0):
#    xrange = "Shut up, linter."
if sys.version_info < (3, 0):
    range = xrange


class MarkovGenerator(object):

    """
    Makes markov-generated output of a given length for a given input.

    Given a source text and a chosen output sentence length, plus the n-gram
    length to build from, creates a re-usable markov chain for generating
    arbitrary output. Output may be created with or without a seed.
    """

    def __init__(self, text, length, ngram=2):
        """
        Create new instance of MarkovGenerator.

        text: The input text data to build the generator upon.
        length: The desired output sentence length.
        ngram: The word-length of ngrams to use for the generator.
        """
        self.text = text
        self.ngram = ngram
        self.length = length
        self.markov_dict = self.make_markov_dict()

    def make_markov_dict(self):
        """
        Generate a dictionary of next-word frequencies following (n-1)-grams.

        Returns a 2-dimensional dictionary mapping (n-1)-length word lists to
        single-word counters, which correspond to the number of times words
        follow n-grams. The default for an as-yet unseen word is zero.

        eg, for n-grams of length 3:
            {'hello my': {'friend': 1, 'nemesis': 2, 'sandwich: 0'}}
        """
        '''returns a dict of {ngram tuple: Counter}
        counting the number of times words follow an ngram'''
        text = self.text
        ngram = self.ngram
        words = nltk.word_tokenize(text)
        zippy_words = zip(*[words[i:] for i in range(ngram + 1)])
        markov_dict = defaultdict(Counter)
        for t in zippy_words:
            a, b = t[:-1], t[-1]
            markov_dict[a][b] += 1
        return markov_dict

    def choose_word(self, start_key):
        """Pick word to follow n-gram based using an accumulate function."""
        def accumulate(iterable, func=operator.add):
            it = iter(iterable)
            total = next(it)
            yield total
            for el in it:
                total = func(total, el)
                yield total
        choices, weights = zip(*self.markov_dict[start_key].items())
        cumulative_distribution = list(accumulate(weights))
        weighted_rando = random.random() * cumulative_distribution[-1]
        return choices[bisect.bisect(cumulative_distribution, weighted_rando)]

    def ngrams_to_words(self, tuple_list):
        """Helper function for generate_words: (list of ngram tuples->str)."""
        word_list = [x[0] for x in tuple_list[1:-1]] + list(tuple_list[-1])
        words = ''
        for i in word_list:
            if i not in string.punctuation:
                words += i + ' '
            else:
                words = words.strip() + i + ' '
        return words.strip()

    # begin hacky text cleanup fuctions!
    def tickmark_cleanup(self, text):
        """Remove empty quotes/backticks, and deduplicate whitespace."""
        no_ticks = re.sub(r"``|''", r"", text)
        fixed = re.sub(r"(\s)\s", r"\1", no_ticks)
        return fixed

    def fix_apostrophes(self, text):
        """Join word-pairs where the second word begins with apostrophe."""
        return re.sub(r"(\w)\s'(\w)", r"\1'\2", text)

    def fix_nt(self, text):
        """Join word-pairs where second word is "n't"."""
        return re.sub(r"(\w)\sn't", r"\1n't", text)

    def final_cleanup(self, text):
        """Fix apostrophes, "n't", and loose tickmarks."""
        return self.tickmark_cleanup(self.fix_apostrophes(self.fix_nt(text)))

    def generate_words(self):
        """Generate new text."""
        start_tups = [k for k in self.markov_dict.keys() if k[0] == '.']
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
        for i in range(4):  # try four times to get a good end of sentence
            if '.' in self.markov_dict[last_tup].values():
                words_tuples.append(('.',))
                generated_text = self.ngrams_to_words(words_tuples)
            else:
                last_word = self.choose_word(last_tup)
                last_tup = last_tup[1:] + (last_word,)
                continue
        words_tuples.append(('.',))
        generated_text = self.ngrams_to_words(words_tuples)
        generated_text[0].upper()
        if generated_text[-2] in string.punctuation:
            generated_text = generated_text[:-2] + '.'
        return self.final_cleanup(generated_text)
