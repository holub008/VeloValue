CREATE TABLE cl_city (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    subdomain VARCHAR(64) NOT NULL
);

CREATE TABLE cl_posting (
    id SERIAL PRIMARY KEY,
    cl_id INTEGER NOT NULL UNIQUE,
    city_id INTEGER REFERENCES cl_cities(id),
    posting_time TIMESTAMP NOT NULL,
    price_usd_cents INTEGER NOT NULL,
    number_of_images INTEGER NOT NULL DEFAULT 0,
    title TEXT NOT NULL,
    description TEXT NOT NULL
);

CREATE cl_posting_attribute (
    id SERIAL PRIMARY KEY,
    posting_id INTEGER REFERENCES cl_posting(id),
    key TEXT NOT NULL,
    value TEXT NOT NULL
)