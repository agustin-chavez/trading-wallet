/* SQL definitions just for reference since SQLAlchemy uses a different approach */

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    encrypted_password TEXT NOT NULL
);

CREATE INDEX idx_users_id ON users (id); /* Recommended */
CREATE INDEX idx_username ON users (username); /* Optimize usernames check on registrations */
CREATE INDEX idx_email ON users (email); /* Optimize emails check on registrations */

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users (id),
    ticker TEXT NOT NULL,
    shares INTEGER NOT NULL,
    share_price NUMERIC NOT NULL,
    fee NUMERIC NOT NULL,
    transaction_date DATE NOT NULL,
);

CREATE INDEX idx_transactions_id ON transactions(id); /* Recommended */
CREATE INDEX idx_user_id ON transactions(user_id); /* Optimize filtering transactions by user_id */

CREATE TABLE holdings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users (id),
    ticker TEXT NOT NULL,
    shares INTEGER NOT NULL DEFAULT 1,
);

CREATE INDEX idx_holdings_id ON holdings(id); /* Recommended */
CREATE INDEX idx_user_id ON holdings(user_id); /* Optimize filtering user's holdings by user_id */