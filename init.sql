CREATE TABLE link (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    long_url VARCHAR(600),
    short_url VARCHAR(40) UNIQUE,
    url_code VARCHAR(10) UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);