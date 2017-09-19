#
# Tests the web scraper.
# Author: Emily Quinn Finney
#
# Fixes:
# Write better tests for this
# Also I should have setup and tear-down functionality since this is writing directly to file
#

import web_scraper as webs


def test_open_page(url='http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType'):
    webs.open_page(url)


def test_locate_linked_pages(url='http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType'):
    webs.locate_linked_pages(url)


def test_filter_pages(url='http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType',
                      sequence='c=NumiTeaStore@ByType'):
    links = webs.filter_pages(url, sequence)
    for link in links:
        assert sequence in link


def test_locate_descriptive_text(url='http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType',
                                 filename='tea_test.txt'):
    link = webs.open_page(url)
    text = webs.locate_descriptive_text(link, filename)
    print(text)


def test_scrape_page(url='http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType',
                     sequence='c=NumiTeaStore@ByType', filename='tea_corpus.txt'):
    webs.scrape_page(url, sequence, filename)
