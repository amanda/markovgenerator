markovgenerator
==============

A Markov text generator written in Python.

The MarkovGenerator class takes a input text to generate sentences from, the length of the output you want (in characters), and an optional ngram length (the default is 2).

Many thanks to @jamak for his help with this!

usage
====

```py
import markov
with open('frankenstein.txt') as f:
    frankenstein = f.read()
markov_gen = markov.MarkovGenerator(text=frankenstein, length=200, ngram=3)
print markov_gen.generate_words()
```

TODO:
====
- ~~fix ending punctuation, don't add a period if there's already something (maybe works now)~~
- figure out what's going on with `` marks
- make a setup.py file
- make pip installable
- pickle input?
