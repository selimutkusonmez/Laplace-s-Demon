-- USERS TABLE --

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username varchar(50) UNIQUE NOT NULL,
    password varchar(255) NOT NULL
);

-- LOGS TABLE --

CREATE TABLE IF NOT EXISTS history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operation varchar(50) NOT NULL,
    inputs TEXT NOT NULL,
    output TEXT NOT NULL,
    chart varchar(255)
)


-- Users -- 

INSERT INTO users (username,password)
VALUES ('d','d')
ON CONFLICT (username) DO NOTHING;