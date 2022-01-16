CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL,
    country TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
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
    domain TEXT NOT NULL,
    endpoint TEXT,
    description TEXT NOT NULL,
    severity TEXT NOT NULL,
    status TEXT NOT NULL,
    date DATE NOT NULL DEFAULT CURRENT_DATE,
    company_name TEXT NOT NULL REFERENCES companies(username),
    user_name TEXT NOT NULL REFERENCES users(username)
);

CREATE TABLE scope (
    id SERIAL PRIMARY KEY,
    url TEXT NOT NULL,
    company_id INTEGER NOT NULL REFERENCES companies(id)
);