
# User status updates
CREATE TABLE updates (
    id bigint,
    state bool,
    time timestamp
);

CREATE INDEX updates_id ON updates(id);
CREATE INDEX updates_time ON updates(time);



# User updates
CREATE TABLE user_updates (
    id bigint,
    time timestamp DEFAULT CURRENT_TIMESTAMP,
    username varchar(32),
    first_name varchar(255),
    last_name varchar(255),
    phone_number varchar(20)
);

CREATE INDEX user_updates_id ON user_updates(id);



# Users
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



# Update user status to offline if it has expired
CREATE PROCEDURE updateUser (
    user_id bigint
)
BEGIN

    SELECT status_online, status_expires
    INTO @status, @expires
    FROM users
    WHERE id = user_id;

    # If online status expired, set to offline
    IF @status = 1 AND @expires < NOW() THEN
        UPDATE users
        SET status_online = 0,
            status_time = @expires,
            status_expires = NULL
        WHERE id = user_id;

        INSERT INTO updates (
            id,
            state,
            time
        )
        VALUES (
            user_id,
            0,
            @expires
        );
    END IF;

END;



# Main procedure for handling user updates
CREATE PROCEDURE handleUserUpdate (
    user_id bigint,
    state bool,
    time timestamp,
    expires timestamp,
    username varchar(32),
    first_name varchar(255),
    last_name varchar(255),
    phone_number varchar(20)
)
BEGIN

    # If user does not exist, create new user
    IF NOT EXISTS(SELECT id FROM users WHERE id = user_id) THEN

        INSERT INTO users (
            id,
            status_online,
            status_time,
            status_expires,
            username,
            first_name,
            last_name,
            phone_number
        )
        VALUES (
            user_id,
            state,
            time,
            expires,
            username,
            first_name,
            last_name,
            phone_number
        );

        INSERT INTO updates (
            id,
            state,
            time
        )
        VALUES (
            user_id,
            state,
            time
        );

    # If user exists, handle update
    ELSE

        SELECT status_online
        INTO @status
        FROM users
        WHERE id = user_id;

        IF @status = state THEN
            IF state = 1 THEN
                # Renew status expiration time
                UPDATE users
                SET status_expires = expires
                WHERE id = user_id;
            END IF;

            UPDATE users
            SET username = username,
                first_name = first_name,
                last_name = last_name,
                phone_number = phone_number
            WHERE id = user_id;
        ELSE
            UPDATE users
            SET status_online = state,
                status_time = time,
                status_expires = expires,
                username = username,
                first_name = first_name,
                last_name = last_name,
                phone_number = phone_number
            WHERE id = user_id;

            INSERT INTO updates (
                id,
                state,
                time
            )
            VALUES (
                user_id,
                state,
                time
            );
        END IF;

    END IF;

END;



# Save user data updates (name, phone number, ...)
CREATE PROCEDURE saveUserUpdate (
    user_id bigint
)
BEGIN

    # Get new user data
    SELECT username, first_name, last_name, phone_number
    INTO @username, @first_name, @last_name, @phone_number
    FROM users
    WHERE id = user_id;

    # Get old user data
    SELECT username, first_name, last_name, phone_number
    INTO @old_username, @old_first_name, @old_last_name, @old_phone_number
    FROM user_updates
    WHERE id = user_id
    ORDER BY time DESC LIMIT 1;

    # Save user update if some user data field has changed
    IF NOT (@username <=> @old_username
        AND @first_name <=> @old_first_name
        AND @last_name <=> @old_last_name
        AND @phone_number <=> @old_phone_number)
    THEN
        INSERT INTO user_updates (
            id,
            username,
            first_name,
            last_name,
            phone_number
        )
        VALUES (
            user_id,
            @username,
            @first_name,
            @last_name,
            @phone_number
        );
    END IF;

END;



# Get user online time for given time period in miliseconds
CREATE FUNCTION getUserOnlineTime(
    user_id bigint,
    from_date datetime,
    to_date datetime
)
RETURNS int
READS SQL DATA
BEGIN
    DECLARE total_sum int;

    SELECT SUM(diff) INTO total_sum
    FROM (
        SELECT UNIX_TIMESTAMP(end_time) - UNIX_TIMESTAMP(start_time) AS diff
        FROM (
            SELECT time AS start_time,
                LEAD(time) OVER (PARTITION BY id ORDER BY time) AS end_time,
                state
            FROM (
                SELECT time,
                    CASE WHEN @prev_state = state THEN @prev_state := @prev_state ELSE @prev_state := state END AS state,
                    id
                FROM updates, (SELECT @prev_state := -1) AS init
                WHERE id = user_id AND time BETWEEN from_date AND to_date
                ORDER BY time
            ) AS subquery
        ) AS subquery2
        WHERE state = 1
    ) AS sums;

    RETURN total_sum;
END;
