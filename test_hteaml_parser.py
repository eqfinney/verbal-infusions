#
# Tests the web scraper.
# Author: Emily Quinn Finney
#
# Fixes:
# I should have a few more tests for the methods in web_scraper: write a mock?
# Need a test for locate_descriptive_text()
# I should have setup and tear-down functionality since this is writing directly to file
#

import hteaml_parser as hp
from bs4 import BeautifulSoup


def test_read_soup(filename='tea_corpus.html'):
    file = hp.read_soup(filename)
    assert type(file[0]) == type(BeautifulSoup('', 'lxml'))
