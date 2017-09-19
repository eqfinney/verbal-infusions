#
# scrapes pages for Verbal Infusions
# Author: Emily Quinn Finney
#
# Fixes:
# 1. Improve tests so they are more meaningful, besides just assuring the function runs
# 2. Make sure the text that's getting scraped is actually what I want to add to the corpus
#


import urllib.request as urq
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re

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


def locate_linked_pages(url, sequence):
    """
    Given a page structured in a Beautiful Soup format, returns all the pages linked
    that contain a given sequence of characters in their URLs.
    :param url: a url for a web page, string
    :param sequence: the sequence to match in each of the chosen URLs
    :return: linked_pages, a list of strings containing linked URLs
    """
    structured_page = open_page(url)
    all_links = structured_page.find_all('a')
    set_of_links = set()
    for link in all_links:
        address = str(link.get('href'))
        if sequence in address:
            if not urlparse(address).netloc:
                scheme = urlparse(url).scheme
                base_url = urlparse(url).netloc
                address = ''.join([scheme, '://', base_url, address])
            set_of_links.add(address)

    return set_of_links


def locate_descriptive_text(structured_page, filename):
    """
    Given a page structured in a Beautiful Soup format, returns all descriptive text on page
    :param structured_page: web page, structured in Beautiful Soup format
    :param filename: the name of the file to which to write the corpus, string
    :return: nothing, but should write a corpus of text from the website to file
    """
    # remove headers from the Beautiful Soup file
    all_text = structured_page.prettify() #get_text(' ', strip=True)
    with open(filename, 'a') as f:
        f.write(all_text)

    return


def scrape_page(url, sequence, id_sequence, filename):
    """
    Scrapes a page and all underlying page whose titles match a certain sequence, writing
    the text results into a text file.
    :param url: the string denoting the base page to scrape
    :param sequence: the sequence any linked URLs must match to be scraped
    :param filename: the filename of the resultant text corpus
    :return: set_of_links, a set of the pages successfully scraped
    """

    master_list = set()
    # find urls in layer 0
    url_list = locate_linked_pages(url, sequence)
    # all urls that haven't yet been seen, which should be everything
    master_list.update(scrape_layer(url_list, master_list, sequence, id_sequence, filename))

    return master_list


def scrape_layer(undiscovered, master_list, sequence, id_sequence, filename):
    """
    Examines each of the pages matching a given sequence on a layer, writing the results to a text file.
    :param undiscovered: the URLs that have not yet been searched
    :param master_list: the URLs that have been searched, no duplicates
    :param sequence: the sequence any linked URLs must match to be scraped
    :param filename: the name of the file to which to write the HTML
    :return:
    """
    print('we have', len(undiscovered), 'objects!')
    url_list = set()

    # return master list if undiscovered is empty
    if not undiscovered:
        return master_list

    else:
        # we want to discover new URLs on each page
        for link in undiscovered:
            id_number = find_id(link, id_sequence)
            if not identify_duplicates(link, master_list, id_sequence):
                master_list.add(id_number)
                print(link)
                page = open_page(link, inspect=False)
                locate_descriptive_text(page, filename)
                url_list.update(locate_linked_pages(link, sequence))

        # recurse to the next layer, looking at only undiscovered links
        undiscovered = (url_list - master_list)
        master_list.update(scrape_layer(undiscovered, master_list, sequence, id_sequence, filename))

        return master_list


def find_id(url, id_sequence):
    """

    :param url:
    :param id_sequence: NUMIS-[0-9]*
    :return:
    """
    # find the parts of the string that match id_sequence
    if re.search(id_sequence, url):
        id = re.search(id_sequence, url).group()
    else:
        id = None
    return id


def identify_duplicates(url, master_list, id_sequence):
    """

    :return:
    """
    id_number = find_id(url, id_sequence)
    if id_number:
        # check that ID against the master_list
        if id_number in master_list:
            return True
        else:
            return False
    # if no ID number, treat the page as a duplicate and don't add it to the list
    else:
        return True


if __name__ == '__main__':
    scrape_page('http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType',
                'c=NumiTeaStore@ByType', 'NUMIS-[0-9]*', 'tea_corpus.txt')
