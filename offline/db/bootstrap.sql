CREATE DATABASE velo_value;

CREATE USER velo_value WITH PASSWORD '';
REVOKE CREATE ON SCHEMA public FROM velo_value;


CREATE TABLE cl_city (
    id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    subdomain VARCHAR(64) NOT NULL
);

CREATE TABLE cl_posting (
    id SERIAL PRIMARY KEY,
    cl_id INTEGER NOT NULL UNIQUE,
    city_id INTEGER REFERENCES cl_city(id),
    posting_time TIMESTAMP NOT NULL,
    price_usd_cents INTEGER NOT NULL,
    number_of_images INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    inserted_at TIMESTAMP NOT NULL DEFAULT NOW()
);

COMMENT ON COLUMN cl_posting.posting_time IS 'local time of posting';

CREATE TABLE cl_posting_attribute (
    id SERIAL PRIMARY KEY,
    posting_id INTEGER REFERENCES cl_posting(id),
    key TEXT NOT NULL,
    value TEXT NOT NULL
);

GRANT SELECT ON ALL TABLES IN SCHEMA public TO velo_value;