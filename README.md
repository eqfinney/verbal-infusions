# Verbal Infusions
Author: Emily Quinn Finney

This package includes code used to support the infrastructure of a Twitter Bot 
(https://twitter.com/verbalinfusions) I wrote during my time at the Recurse 
Center (https://www.recurse.com/).

## Features/Details 

The package includes the following modules:

* create_status.py: implements a Markov chain from which herbal tea parody 
tweets are generated. 
* hteaml_parser.py: parses a corpus of HTML using Python's Beautiful Soup
and re packages. Apologies for the pun are not included.
* twitter_bot.py: the infrastructure for the Twitter Bot, written using the
Tweepy package that wraps the Twitter API (http://www.tweepy.org/).

## Running Tests

The modules test_*.py are pytest modules that test the code corresponding to their names. To test the code, you will need pytest installed. Then type the following into the terminal: 

```
pytest -v -s test_{$MODULE_NAME}.py
```

Last edited 04/05/2018