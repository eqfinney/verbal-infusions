#
# scrapes pages for Verbal Infusions
# Author: Emily Quinn Finney
#
# Fixes:
# Refactor a few functions so that their purpose is obvious and as generalizable as possible
#


import web_crawler as wc
from bs4 import BeautifulSoup
import re

try:
    import psyco
    psyco.full()
except ImportError:
    pass


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
        structured_pages.append(BeautifulSoup(''.join([html_header, web_page]), 'lxml'))
    return structured_pages


def locate_descriptive_text(filename, structured_page, tag_pattern, tag_names):
        """
        Given a page structured in a Beautiful Soup format, returns all descriptive text on page
        :param structured_page: list of web pages, structured in Beautiful Soup format
        :return: nothing, but should write a corpus of text to file
        """
        with open(filename, 'a') as f:
            # identify all descriptions on web page matching the pattern in the PageScraper object
            prod_description = structured_page.find_all('div', class_=re.compile(tag_pattern))
            # then go through them
            # this method is going to depend on the structure of the web page
            # so I'm not sure how I would generalize it
            for prod in prod_description:
                if prod['class'][0] == tag_names[0]:
                    for element in prod:
                        if element.string:
                            f.write(element.string)
                elif prod['class'][0] == tag_names[1]:
                    if prod.ul:
                        for child in prod.ul.children:
                            if child:
                                if child.string:
                                    f.write(child.string)
                else:
                    pass


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
    NumiTeaScraper = wc.PageScraper('http://shop.numitea.com/Tea-by-Type/c/NumiTeaStore@ByType',
                                    'c=NumiTeaStore@ByType', 'NUMIS-[0-9]*', 'tea_corpus.txt',
                                    ('product_description', 'tab_content'), "product")
    NumiTeaScraper.scrape_page()