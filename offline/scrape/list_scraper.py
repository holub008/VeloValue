import re
import math
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup

_MAIN_PAGE_URL = "http://minneapolis.craigslist.org/"
_LIST_URL_FORMAT = "https://%s.craigslist.org/search/bia?s=%d"
_LIST_PAGE_SIZE = 120
# it seems CL limits active listings to 3000
_MAX_PAGES = math.ceil(3000 / _LIST_PAGE_SIZE)
_MILLIS_BETWEEN_REQUESTS = 100


def _extract_city_subdomain(url):
    matches = re.match(r'^https?://([a-z]+)\.craigslist\.org/$', url)
    if matches:
        return matches.group(1)

    raise ValueError('Unable to extract city subdomain from main url')


def get_main_cities():
    """
    :return: DataFrame
    """
    res = requests.get(_MAIN_PAGE_URL)
    soup = BeautifulSoup(res.content, 'lxml')
    cities_header = soup.find('h5', text='us cities')
    if not cities_header:
        raise ValueError('Unable to extract expected cities listing on homepage.')

    cities_list = cities_header.findNext('ul')
    parsed_cities = [(a.text, _extract_city_subdomain(a['href']))
                     for a in cities_list.find_all('a') if not a.text == 'more ...']

    return pd.DataFrame(parsed_cities, columns=['name', 'subdomain'])


def _parse_listing_li(li):
    pid = int(li['data-pid'])
    parent_pid = int(li['data-repost-of']) if li.has_attr('data-repost-of') else None
    title_a = li.find('a', {'class': 'result-title hdrlnk'})

    if not title_a:
        raise ValueError('Unable to find title element in list page posting!')

    return pid, parent_pid, title_a['href']


def get_listed_postings(city_subdomain):
    """
    note this function may miss postings at any position in the list due to
    1. new posts being added 2. existing posts being deleted
    :param city_subdomain: the subdomain of the city to scrape
    :return: a dataframe with pointers to all postings to scrape
    """
    all_postings = []
    for page_ix in range(0, _MAX_PAGES + 1):
        url = _LIST_URL_FORMAT % (city_subdomain, page_ix * _LIST_PAGE_SIZE)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        postings_list = soup.find('ul', {'class': 'rows'})
        posting_entries = postings_list.find_all('li', {'class': 'result-row'})
        postings_parsed = [_parse_listing_li(li) for li in posting_entries]
        if not len(postings_parsed):
            break
        all_postings += postings_parsed
        time.sleep(_MILLIS_BETWEEN_REQUESTS / 1000)

    return pd.DataFrame(all_postings, columns=['cl_id', 'parent_cl_id', 'posting_url'])






