#
# creates statuses for the Verbal Infusions Twitter account
# Author: Emily Quinn Finney
#

from collections import Counter
from collections import defaultdict
import random


def read_words(filename):
    """
    Reads the text in a corpus, doing some basic preprocessing
    :param filename:
    :return:
    """
    with open(filename, 'r') as f:
        page = f.read()

    # create a list of lines so that each new line ends in a period.
    linelist = page.splitlines()
    newpage = ''

    for value in linelist:
        if value.isspace() or value == '':
            continue

        # remove whitespace from each line
        value = value.lstrip()
        value = value.rstrip()

        # add a period to the end of the line if it's not there already
        if value[-1] != '.':
            newline = ''.join([value, '.'])
            newpage = ' '.join([newpage, newline])
        else:
            newpage = ' '.join([newpage, value])

    words = newpage.split()

    return words


def make_dictionary(filename):
    """
    Makes a dictionary of Counters from a given text corpus.
    At the end of a sentence, should return any value that starts a sentence.
    :param filename: the name of the file from which to read, string
    :return: a dictionary, with words as keys and Counter objects as values
    """
    words = read_words(filename)
    dictionary = defaultdict(list)

    # we set '*' to be the value that starts a sentence
    prev_word = '*'

    for word in words:

        if word == 'Numi':
            word = 'FancyTea'
        if word == 'Numi\'s':
            word = 'FancyTea\'s'

        # create a default dict entry for the previous
        if dictionary[prev_word]:
            # prev_word should be a key, value is Counter with list of words
            dictionary[prev_word][word] += 1
        else:
            dictionary[prev_word] = Counter({word: 1})

        # test to see if that word ends the sentence
        if word[-1] == '.':
            # if yes, set prev_word to be the sentence-beginning keyword
            prev_word = '*'
        else:
            # if no, set prev_word to be word
            prev_word = word

    return dictionary


def markov_tweet(filename):
    """
    Creates a Markov-generated 140-character string based on a text corpus.
    :param filename: the name of the text corpus from which to generate the tweet, string
    :return: a 140-character or fewer string to be tweeted to the world
    """

    dictionary = make_dictionary(filename)

    words = list(dictionary['*'].elements())
    seed_word = random.choice(words)

    string = seed_word

    while len(string) < 140:

        # make sure the dictionary entry exists
        if dictionary[seed_word]:
            new_list = list(dictionary[seed_word].elements())
            new_word = random.choice(new_list)

            # what to do if the new word isn't the new sentence character
            if new_word != '*':
                string = ' '.join([string, new_word])

                # edge case: nearing the end of a tweet
                if len(string) > 140:
                    stringlist = string.split('.')
                    if stringlist[-1] != '':
                        string = '.'.join(stringlist[:-1])
                    else:
                        string = '.'.join(stringlist[:-2])
                    if string[-1:] != '.':
                        string = ''.join([string, '.'])
                    break

            # update the word for future use
            seed_word = new_word

        # if no word in the dictionary, treat as a new sentence
        else:
            seed_word = '*'

    print(string)
    return string


if __name__ == '__main__':
    markov_tweet('tea_description.txt')
