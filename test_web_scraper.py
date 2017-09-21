#
# Tests the web scraper.
# Author: Emily Quinn Finney
#
# Fixes:
# I should have a few more tests for the methods in web_scraper: write a mock?
# I should have setup and tear-down functionality since this is writing directly to file
#

import web_scraper as webs
from bs4 import BeautifulSoup


def test_open_page(url='http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType'):
    webs.open_page(url)


def test_locate_linked_pages(url='http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType',
                             sequence='c=NumiTeaStore@ByType'):
    set_of_links = webs.locate_linked_pages(url, sequence)
    for thing in set_of_links:
        assert sequence in thing


def test_read_soup(filename='tea_corpus.html'):
    file = webs.read_soup(filename)
    assert type(file[0]) == type(BeautifulSoup('', 'lxml'))


def test_find_id(url='http://shop.numitea.com/NUMIS-10430&c=NumiTeaStore@ByType@Puerh',
                 id_sequence='NUMIS-[0-9]*'):
    value = webs.find_id(url, id_sequence)
    assert value == 'NUMIS-10430'


def test_identify_duplicates(url='http://shop.numitea.com/NUMIS-10430&c=NumiTeaStore@ByType@Puerh',
                             master_list={'NUMIS-10430'}, id_sequence='NUMIS-[0-9]*'):
    truefalse = webs.identify_duplicates(url, master_list, id_sequence)
    assert truefalse
