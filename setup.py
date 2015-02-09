from setuptools import setup, find_packages
from codecs import open 
from os import path

here = path.abspath(path.dirname(__file__))

setup(
  name = 'markovgenerator',
  version = '0.0.2',
  description = 'Markov text generator',
  license = 'MIT',
  author = 'Amanda Pickering',
  author_email = 'pickering.amanda@gmail.com',
  install_requires = ['nltk', 'wsgiref'],
  url = 'https://github.com/amandapickering/markovgenerator',
  keywords = 'markov text generator natural language processing generative',
  packages = find_packages(),
)
