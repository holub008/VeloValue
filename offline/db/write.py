import psycopg2.extras as pge
import pandas as pd

from db.connection import get_connection


def insert_and_cities(cities, page_size = 1000):
    required_columns = ['name', 'subdomain']
    values_for_insert = values_for_insert[required_columns]

    with get_connection() as con:
        with con.cursor as cursor:
            query_value_format = "INSERT INTO cl_city (name, subdomain) VALUES %s RETURNING *"
            inserted_values = pge.execute_values(cursor, query_value_format, values_for_insert, fetch = True)
            return pd.DataFrame(inserted_values, columns = required_columns)


def insert_postings(scraped_postings):
    with get_connection() as con:
        with con.cursor as cursor:
            for posting in scraped_postings:
                posting.insert(cursor)
