#
# Tests the Markov chain
# Author: Emily Quinn Finney
#

import create_status as cs


def test_read_words(filename='thirteen_words.txt'):
    words = cs.read_words(filename)
    assert '\n' not in words


def test_make_dictionary(filename='thirteen_words.txt'):
    result = cs.make_dictionary(filename)
    print(result)
    assert 'said' in result['mother']
    assert 'And' in result['*']


def test_markov_tweet(filename='thirteen_words.txt'):
    new_tweet = cs.markov_tweet(filename)
    print(new_tweet)
    assert len(new_tweet) <= 140
    assert new_tweet[-1] == '.'
