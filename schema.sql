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
    drink_type TEXT,
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    review_id INTEGER REFERENCES reviews,
    user_id INTEGER REFERENCES users,
    comment TEXT
);