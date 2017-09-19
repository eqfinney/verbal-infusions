#
# scrapes pages for Verbal Infusions
# Author: Emily Quinn Finney
#
# Fixes:
# 1. Improve tests so they are more meaningful, besides just assuring the function runs
# 2. Remove duplicates from getting scraped, using some funky regex thang
# 3. Make sure the text that's getting scraped is actually what I want to add to the corpus
#


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


def scrape_page(url, sequence, filename):
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
    undiscovered = url_list - master_list
    master_list.update(scrape_layer(undiscovered, master_list, sequence, filename))

    return master_list


def scrape_layer(undiscovered, master_list, sequence, filename):
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
            print(link)
            page = open_page(link, inspect=False)
            locate_descriptive_text(page, filename)
            master_list.add(link)
            url_list.update(locate_linked_pages(link, sequence))

        # recurse to the next layer, looking at only undiscovered links
        undiscovered = (url_list - master_list)
        master_list.update(scrape_layer(undiscovered, master_list, sequence, filename))

        return master_list


if __name__ == '__main__':
    scrape_page('http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType',
                'c=NumiTeaStore@ByType', 'tea_corpus.txt')
