CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    drink TEXT,
    score INTEGER,
    review TEXT,
    user_id INTEGER REFRENCES users
);