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
    preferred_language varchar(10) DEFAULT 'en' NOT NULL,
    preferred_theme varchar(10) DEFAULT 'dark',
    preferred_font_color varchar(50) DEFAULT '#ADBAC7'
);

-- USER STATS TABLE --
CREATE TABLE IF NOT EXISTS user_stats (
    user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
    account_opening_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_successful_login_date TIMESTAMP DEFAULT NULL,
    last_successful_login_ip varchar(255) DEFAULT NULL,
    last_successful_login_mac varchar(255) DEFAULT NULL,
    last_failed_login_date TIMESTAMP DEFAULT NULL,
    last_failed_login_ip varchar(255) DEFAULT NULL,
    last_failed_login_mac varchar(255) DEFAULT NULL,
    total_operation_usage INTEGER DEFAULT 0,
    operation_usage_counts JSONB DEFAULT '{}'::jsonb,
    most_used_operation varchar(50) DEFAULT NULL,
    last_used_operation varchar(50) DEFAULT NULL
);

CREATE OR REPLACE FUNCTION create_user_profiles()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO user_preferences (user_id) 
    VALUES (NEW.id);

    INSERT INTO user_stats (user_id) 
    VALUES (NEW.id);

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_user_registration
AFTER INSERT ON users
FOR EACH ROW
EXECUTE FUNCTION create_user_profiles();

CREATE OR REPLACE FUNCTION update_login_telemetry()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.attempt = 'successful' THEN
        UPDATE user_stats
        SET last_successful_login_date = NEW.date,
            last_successful_login_ip = NEW.ip_adress,
            last_successful_login_mac = NEW.mac_adress
        WHERE user_id = NEW.user_id;
        
    ELSIF NEW.attempt = 'failed' THEN
        UPDATE user_stats
        SET last_failed_login_date = NEW.date,
            last_failed_login_ip = NEW.ip_adress,
            last_failed_login_mac = NEW.mac_adress
        WHERE user_id = NEW.user_id;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_login_attempt
AFTER INSERT ON logs
FOR EACH ROW
EXECUTE FUNCTION update_login_telemetry();


INSERT INTO users (username, password)
VALUES ('d', 'd')
ON CONFLICT (username) DO NOTHING;