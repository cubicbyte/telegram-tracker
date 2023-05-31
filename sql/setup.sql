
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

        # Update expired status
        CALL updateUser(user_id);

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

    CALL saveUserUpdate(user_id);

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
    WHERE id = user_id;

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
