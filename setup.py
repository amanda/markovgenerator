from setuptools import setup, find_packages

setup(
  name = 'markovgenerator',
  version = '0.1',
  description = 'Markov text generator',
  license = 'MIT',
  author = 'Amanda Pickering',
  author_email = 'pickering.amanda@gmail.com',
  install_requires = ['nltk==3.0.1', 'wsgiref==0.1.2'],
  url = 'https://github.com/amandapickering/markovgenerator',
  keywords = 'markov text generator natural language processing generative',
  packages = find_packages(),
)
