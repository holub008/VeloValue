import psycopg2 as pg


def get_connection(host='db.birkielolcom',
                   username='velo_value',
                   database='velo_value',
                   port=5432):
    return pg.connect(dbname=database, user=username, host=host, port=port)
