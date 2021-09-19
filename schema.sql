CREATE TABLE coffees (
    id SERIAL PRIMARY KEY,
    name TEXT,
    creator_id INTEGER REFERENCES users
)

CREATE TABLE rating (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    cafe_id INTEGER REFERENCES cafes,
    rating INTEGER
)

CREATE TABLE recipes (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    coffee_id INTEGER REFERENCES coffees,
    recipe TEXT
)

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT,
    role INTEGER
)

CREATE TABLE cafes (
    id SERIAL PRIMARY KEY,
    name TEXT,
    city TEXT,
    website TEXT,
)

