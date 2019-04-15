import re

import pandas as pd
import requests
from bs4 import BeautifulSoup


def _extract_attribute_pairing(blob):
    matches = re.match(r'^([a-zA-Z0-9\.\- ]+): ([[a-zA-Z0-9\.\- ]+)$', blob)
    if not matches:
        return None, None
    else:
        return matches.group(1), matches.group(2)


def get_posting(posting_url):
    res = requests.get(posting_url)
    soup = BeautifulSoup(res.text, 'lxml')

    time_element = soup.find('time', {'class': 'date timeago'})
    if not time_element:
        raise ValueError('Posting does not have expected time stamp')
    # TODO how to handle timezones? :(
    posting_time = time_element['datetime']

    title_span = soup.find('span', {'id': 'titletextonly'})
    if not title_span:
        raise ValueError('Posting does not have expected title structure')
    title = title_span.text

    price_span = soup.find('span', {'class': 'price'})
    if not price_span:
        raise ValueError('Posting does not have expected price structure')
    price_text = price_span.text
    matches = re.match(r'^\$([0-9\.]+)$', price_text)
    if not matches:
        raise ValueError('Posting does not have expected price string format')
    price_usd = float(matches.group(1))

    image_holder = soup.find('div', {'class': 'slide'})
    if image_holder:
        number_of_images = len(image_holder.find_all('div', {'class': 'slide'}))
    else:
        number_of_images = 0

    attribute_list = soup.find('p', {'class': 'attrgroup'})
    if not attribute_list:
        attributes = {}
    else:
        attribute_spans = attribute_list.find_all('span')
        attributes_tuples = [_extract_attribute_pairing(span.text) for span in attribute_spans]
        attributes = {at[0]: at[1] for at in attributes_tuples}

    review_section = soup.find('section', {'id': 'postingbody'})
    if not review_section:
        raise ValueError('Posting does not have expected description structure')

    # TODO is the QR code crap always the first child element?
    # TODO do we want to maintain some of the hypertext aspects in the review text?
    review_text = review_section.contents[2:]

    return posting_time, title, price_usd, number_of_images, attributes, review_text
