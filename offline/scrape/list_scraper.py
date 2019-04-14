import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

_MAIN_PAGE_URL = "http://minneapolis.craigslist.org/"
_LIST_URL_FORMAT = "https://%s.craigslist.org/search/bia?s=%d"
_LIST_PAGE_SIZE = 120


def _extract_city_subdomain(url):
    matches = re.match(r'^https?://([a-z]+)\.craigslist\.org/$', url)
    if matches:
        return matches.group(1)

    raise ValueError('Unable to extract city subdomain from main url')


def get_main_cities():
    req = requests.get(_MAIN_PAGE_URL)
    soup = BeautifulSoup(req.content, 'lxml')
    cities_header = soup.find('h5', text='us cities')
    if not cities_header:
        raise ValueError('Unable to extract expected cities listing on homepage.')

    cities_list = cities_header.findNext('ul')
    parsed_cities = [(a.text, _extract_city_subdomain(a['href']))
                     for a in cities_list.find_all('a') if not a.text == 'more ...']

    return pd.DataFrame(parsed_cities, columns=['name', 'subdomain'])


def get_listed_postings(cityname):
    pass


