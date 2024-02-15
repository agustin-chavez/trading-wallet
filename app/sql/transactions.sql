CREATE TABLE transactions (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users (id),
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL,
    share_price NUMERIC NOT NULL,
    fee NUMERIC NOT NULL,
    transaction_date DATE NOT NULL,
);

CREATE INDEX idx_transactions_id ON transactions(id); /* Recommended */
CREATE INDEX idx_user_id ON transactions(user_id); /* Optimize filtering transactions by user_id */
