CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    country TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    country TEXT NOT NULL,
    role TEXT NOT NULL,
    full_name TEXT,
    twitter TEXT,
    website TEXT
);

CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    endpoint TEXT,
    description TEXT NOT NULL,
    score INTEGER NOT NULL,
    company_id INTEGER NOT NULL REFERENCES companies(id),
    user_id INTEGER REFERENCES users(id)
);