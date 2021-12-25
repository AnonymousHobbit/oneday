CREATE TABLE company (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    country TEXT,
    full_name TEXT,
    twitter TEXT,
    website TEXT
);

CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL REFERENCES company(id),
    rating DECIMAL NOT NULL,
    content TEXT NOT NULL,
    author_id INTEGER REFERENCES users(id)
);