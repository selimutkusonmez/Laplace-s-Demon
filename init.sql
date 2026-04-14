-- USERS TABLE --
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username varchar(50) UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- HISTORY TABLE --
CREATE TABLE IF NOT EXISTS operation_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    operation varchar(50) NOT NULL,
    variables varchar(255),
    input_data TEXT NOT NULL,
    output TEXT NOT NULL
);

-- LOGS TABLE --
CREATE TABLE IF NOT EXISTS logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    ip_adress varchar(255),
    mac_adress varchar(255),
    attempt varchar(20),
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- USER PREFERENCES TABLE --
CREATE TABLE IF NOT EXISTS user_preferences (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    language_preference varchar(10) DEFAULT 'en' NOT NULL,
    theme varchar(10) DEFAULT 'dark',
    font_color varchar(50) DEFAULT '#ADBAC7'
);

-- USER STATS TABLE --
CREATE TABLE IF NOT EXISTS user_stats (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    account_opening_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_successful_login_date TIMESTAMP,
    last_successful_login_ip varchar(255),
    last_successful_login_mac varchar(255),
    last_failed_login_date TIMESTAMP,
    last_failed_login_ip varchar(255),
    last_failed_login_mac varchar(255),
    total_operation_usage INTEGER DEFAULT 0,
    operation_usage_counts JSONB DEFAULT '{}'::jsonb,
    most_used_operation varchar(50),
    last_used_operation varchar(50)
);

INSERT INTO users (username, password)
VALUES ('d', 'd')
ON CONFLICT (username) DO NOTHING;