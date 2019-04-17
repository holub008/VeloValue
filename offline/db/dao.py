import pandas as pd


def get_cities(cursor):
    query = "SELECT id, name, subdomain from cl_city"
    cursor.execute(query)
    results = cursor.fetchall()

    return pd.DataFrame(results, columns=['city_id', 'city_name', 'subdomain'])


def get_most_recent_cl_ids(cursor):
    pass


def get_all_cl_ids(cursor):
    pass


def get_all_postings(cursor):
    pass
