markovgenerator
==============

A (WIP) Markov text generator written in Python. 

The MarkovGenerator class takes a input text to generate sentences from, the length of the output you want (in characters), and an optional ngram length (the default is 2).

Many thanks to @jamak for help with the math to choose a good next word and @davoclavo for help making it pip installable!

installation
-----------

using pip:
```
pip install markovgenerator
```

or clone the repo and install:
```
python setup.py install
```

usage
----

Example: Generate 200-character sentences from Mary Shelley's _Frankenstein_ based on an ngram length of 3

```py
import markovgenerator

with open('frankenstein.txt') as f:
	frankenstein = f.read()

markov_gen = markovgenerator.MarkovGenerator(frankenstein, 200, 3)

markov_gen.generate_words()
```

returns:
"The weather was fine; it was about the commission of his crimes, and I did right in refusing, to create a companion for the first creature. He showed unparalleled malignity and selfishness in evil."

Using an ngram of 2 (the default), the results get a bit more jibberish-y:
"Clerval had never yet been able to perform it myself! I could banish disease from the first lesson; most of all the voyages made for purposes of discovery, he ceased to fear or to bend beneath words."


TODO:
----
- ~~fix ending punctuation, don't add a period if there's already something (maybe works now)~~
- figure out what's going on with `` marks
- fix spaces before apostrophes (regex)
- ~~make a setup.py file~~
- ~~make pip installable~~
- pickle input?
