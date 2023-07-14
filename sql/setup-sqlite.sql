
-- User status updates
CREATE TABLE updates (
    id bigint,
    state bool,
    time timestamp
);

CREATE INDEX updates_id ON updates(id);
CREATE INDEX updates_time ON updates(time);


-- User info updates
CREATE TABLE user_updates (
    id bigint,
    time timestamp DEFAULT CURRENT_TIMESTAMP,
    username varchar(32),
    first_name varchar(255),
    last_name varchar(255),
    phone_number varchar(20)
);

CREATE INDEX user_updates_id ON user_updates(id);


-- Users
CREATE TABLE users (
    id bigint PRIMARY KEY,
    status_online bool,
    status_time timestamp,
    status_expires timestamp,
    username varchar(32),
    first_name varchar(255),
    last_name varchar(255),
    phone_number varchar(20)
);
