CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    encrypted_password TEXT NOT NULL
);

CREATE INDEX idx_users_id ON users (id); /* Recommended */
CREATE INDEX idx_username ON users (username); /* Optimize usernames check on registrations */
CREATE INDEX idx_email ON users (email); /* Optimize emails check on registrations */
