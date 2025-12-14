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
    user_id INTEGER REFERENCES users(id)
);

CREATE TABLE review_classes (
    id INTEGER PRIMARY KEY,
    review_id INTEGER REFERENCES reviews(id),
    title TEXT,
    value TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    review_id INTEGER REFERENCES reviews(id),
    user_id INTEGER REFERENCES users(id),
    comment TEXT
);