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


def test_find_id(url='http://shop.numitea.com/NUMIS-10430&c=NumiTeaStore@ByType@Puerh',
                 id_sequence='NUMIS-[0-9]*'):
    value = hp.find_id(url, id_sequence)
    assert value == 'NUMIS-10430'


def test_identify_duplicates(url='http://shop.numitea.com/NUMIS-10430&c=NumiTeaStore@ByType@Puerh',
                             master_list={'NUMIS-10430'}, id_sequence='NUMIS-[0-9]*'):
    truefalse = hp.identify_duplicates(url, master_list, id_sequence)
    assert truefalse
