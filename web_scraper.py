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


class PageScraper:

    def __init__(self, url, sequence, id_sequence, filename):
        """
        Initializes the PageScraper class.
        :param url: the base URL from which to scrape, string
        :param sequence: the sequence to which all URLs must be matched if they are to be scraped, string
        :param id_sequence: the sequence used to identify a product ID, string
        :param filename: the filename into which to scrape the website information, string
        """
        self.url = url
        self.sequence = sequence
        self.id_sequence = id_sequence
        self.filename = filename
        # keeps track of all URLs that have been visited so far
        self.master_list = set()

    def scrape_page(self):
        """
        Scrapes a page and all underlying page whose titles match a certain sequence, writing
        the text results into a text file.
        :return: set_of_links, a set of the pages successfully scraped
        """

        # find urls in layer 0
        undiscovered = locate_linked_pages(self.url, self.sequence)
        # all urls that haven't yet been seen, which should be everything
        self.master_list.update(self.scrape_layer(undiscovered))

    def scrape_layer(self, undiscovered):
        """
        Examines each of the pages matching a given sequence on a layer, writing the results to a text file.
        :param undiscovered: the URLs that have not yet been searched
        :return:
        """
        print('we have', len(undiscovered), 'objects!')
        url_list = set()

        # return master list if undiscovered is empty
        if not undiscovered:
            return self.master_list

        else:
            # we want to discover new URLs on each page
            for link in undiscovered:
                id_number = find_id(link, self.id_sequence)
                if not identify_duplicates(link, self.master_list, self.id_sequence):
                    self.master_list.add(id_number)
                    print(link)
                    page = open_page(link, inspect=False)
                    locate_descriptive_text(page, self.filename)
                    url_list.update(locate_linked_pages(link, self.sequence))

            # recurse to the next layer, looking at only undiscovered links
            undiscovered = (url_list - self.master_list)
            self.master_list.update(self.scrape_layer(undiscovered))

            return self.master_list


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


def read_soup(filename):
    """
    Given a text file structured as prettified Beautiful Soup HTML, returns a Beautiful Soup object
    :param filename: the name of the file from which to read the HTML
    :return: structured_page, the Beautiful Soup object
    """
    with open(filename, 'r') as f:
        page = f.read()

    html_header = "<!DOCTYPE html>"
    all_pages = page.split(sep=html_header)
    # turn text file into a Beautiful Soup object
    structured_pages = []
    for web_page in all_pages[1:]:
        structured_pages.append(BeautifulSoup(''.join([html_header,web_page]), 'lxml'))
    return structured_pages


def locate_descriptive_text(structured_page, filename):
    """
    Given a page structured in a Beautiful Soup format, returns all descriptive text on page
    :param structured_pages: list of web pages, structured in Beautiful Soup format
    :param filename: the name of the file to which to write the corpus, string
    :return: nothing, but should write a corpus of text to file
    """
    with open(filename, 'a') as f:
        prod_description = structured_page.find_all('div', class_=re.compile("product"))
        for prod in prod_description:
            if prod['class'][0] == "product_description":
                for element in prod:
                    if element.string:
                        f.write(element.string)
            elif prod['class'][0] == "tab_content":
                if prod.ul:
                    for child in prod.ul.children:
                        if child:
                            if child.string:
                                print(child.string)
                                f.write(child.string)
            else:
                pass

    return


def find_id(url, id_sequence):
    """
    Matches the identification sequence in a URL, returning the ID number in the URL
    :param url: a URL from which to draw a product ID number
    :param id_sequence: the identification sequence used to ID products in a URL
    :return: id_number, the ID number of the product referenced in the URL
    """
    # find the parts of the string that match id_sequence
    if re.search(id_sequence, url):
        id_number = re.search(id_sequence, url).group()
    else:
        id_number = None
    return id_number


def identify_duplicates(url, master_list, id_sequence):
    """
    Determines whether the product has already been included in a master list of products.
    :param url: a URL from which to draw a product ID number
    :param master_list: the master list of products with which to compare the product ID
    :param id_sequence: the ID sequence used to ID products in a URL
    :return: a Boolean showing whether the product has been seen (T) or not (F)
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
    NumiTeaScraper = PageScraper('http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType',
                                 'c=NumiTeaStore@ByType', 'NUMIS-[0-9]*', 'tea_corpus.txt')
    NumiTeaScraper.scrape_page()
