CREATE TABLE holdings (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users (id),
    symbol TEXT NOT NULL,
    shares INTEGER NOT NULL DEFAULT 1,
);

CREATE INDEX idx_holdings_id ON holdings(id); /* Recommended */
CREATE INDEX idx_user_id ON holdings(user_id); /* Optimize filtering user's holdings by user_id */