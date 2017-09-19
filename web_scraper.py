#
# scrapes pages for Verbal Infusions
# Author: Emily Quinn Finney
#
# Fixes:
# 1. Improve tests so they are more meaningful, besides just assuring the function runs
# 2. Currently, this code is ABSURDLY SLOW which makes sense since I use too many for loops
# 3. Improve scraping functionality so that it can scrape nested pages
# 4. Make sure the text that's getting scraped is actually what I want to add to the corpus

"""
1. Make sure I hit every node at least once.
2. When I hit a node:
   a. Make sure I mark the node as having been hit.
   b. Make sure I scrape the text on the page.
Node = web page. Edge = URL to another web page.
This is a directed graph, so there's that to consider.
"""


import urllib.request as urq
from urllib.parse import urlparse
from bs4 import BeautifulSoup

try:
    import psyco
    psyco.full()
except ImportError:
    pass


def open_page(url, inspect=False):
    """
    Opens a web page using the urllib.request library, and returns a Beautiful Soup object
    :param url: string, the URL of the web page of interest.
    :param inspect: boolean, determines whether or not to print the prettified nested HTML page
    :return: structured_page, the BeautifulSoup object
    """
    page = urq.urlopen(url)
    structured_page = BeautifulSoup(page, 'lxml')
    if inspect is True:
        print(structured_page.prettify())
    return structured_page


def locate_linked_pages(url):
    """
    Given a page structured in a Beautiful Soup format, returns all the pages linked
    :param url: a url for a web page, string
    :return: linked_pages, a list of strings containing linked URLs
    """
    structured_page = open_page(url)
    all_links = structured_page.find_all('a')
    set_of_links = set()
    for link in all_links:
        address = link.get('href')
        if address:
            if not urlparse(address).netloc:
                scheme = urlparse(url).scheme
                base_url = urlparse(url).netloc
                address = ''.join([scheme, '://', base_url, address])
            set_of_links.add(address)

    return set_of_links


def filter_pages(url, sequence):
    """
    Given a page structured in Beautiful Soup format, returns all pages linked that contain
    a given sequence of characters in their URLs.
    :param url: a url for a web page, string
    :param sequence: the sequence to match in each of the chosen URLs
    :return: url_list, a list of URLs that contain a matching sequence
    """
    links = locate_linked_pages(url)
    url_list = set()
    { url_list.add(link) for link in links if sequence in link }
    #print(url_list)

    return url_list


def locate_descriptive_text(structured_page, filename):
    """
    Given a page structured in a Beautiful Soup format, returns all descriptive text on page
    :param structured_page: web page, structured in Beautiful Soup format
    :param filename: the name of the file to which to write the corpus, string
    :return: nothing, but should write a corpus of text from the website to file
    """
    # remove headers from the Beautiful Soup file
    all_text = structured_page.get_text(' ', strip=True)
    #print(all_text)
    with open(filename, 'w') as f:
        f.write(all_text)

    return


def scrape_page(url, sequence, filename, master_list=set(), inspect=False):
    """
    Scrapes a page and all underlying page whose titles match a certain sequence, writing
    the text results into a text file.
    :param url: the string denoting the base page to scrape
    :param sequence: the sequence any linked URLs must match to be scraped
    :param filename: the filename of the resultant text corpus
    :param inspect: boolean, whether or not to inspect each page
    :return: set_of_links, a set of the pages successfully scraped
    """

    links = filter_pages(url, sequence)

    if links.issubset(master_list):
        return master_list

    else:
        new_list = scrape_page(link, sequence, filename, master_list)
        page = open_page(link, inspect=inspect)
        locate_descriptive_text(page, filename)


if __name__ == '__main__':
    scrape_page('http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType',
                'c=NumiTeaStore@ByType', 'tea_corpus.txt')
