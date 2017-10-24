## Verbal Infusions
Author: Emily Quinn Finney

This package includes code used to support the infrastructure of a Twitter Bot 
(https://twitter.com/verbalinfusions) I wrote during my time at the Recurse 
Center (https://www.recurse.com/). The package includes:

* create_status.py: implements a Markov chain from which herbal tea parody 
tweets are generated. 
* hteaml_parser.py: parses a corpus of HTML using Python's Beautiful Soup
and re packages. Apologies for the pun are not included.
* twitter_bot.py: the infrastructure for the Twitter Bot, written using the
Tweepy package that wraps the Twitter API (http://www.tweepy.org/).
* test_*.py: pytest modules that test the code corresponding to their names.

Last edited 10/24/2017