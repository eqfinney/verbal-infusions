#
# scrapes pages for Verbal Infusions
# Author: Emily Quinn Finney
#
# Fixes:
# Refactor a few functions so that their purpose is obvious and as generalizable as possible
#


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


def locate_descriptive_text(structured_page, tag_pattern, tag_names, filename):
        """
        Given a page structured in a Beautiful Soup format, returns all descriptive text on page
        :param structured_page: list of web pages, structured in Beautiful Soup format
        :param tag_pattern: string, the HTML tag pattern for which to search
        :param tag_names: tuple of strings, the names of the relevant HTML tags to write
        :param filename: string, the name of the file to which to write the text
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
