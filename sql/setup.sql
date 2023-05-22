
CREATE TABLE updates (
    id bigint,
    state bool,
    time timestamp
);

CREATE INDEX updates_id ON updates(id);
CREATE INDEX updates_time ON updates(time);



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



CREATE PROCEDURE updateUser (
    user_id bigint
)
BEGIN

    SELECT status_online, status_expires
    INTO @status, @expires
    FROM users
    WHERE id = user_id;

    IF @status = 1 THEN
        IF @expires < NOW() THEN
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
    END IF;

END;



CREATE PROCEDURE handleUserUpdate (
    user_id bigint,
    state bool,
    time timestamp,
    expires timestamp,
    username varchar(255),
    first_name varchar(255),
    last_name varchar(255),
    phone_number varchar(20)
)
BEGIN

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

    ELSE

        CALL updateUser(user_id);

        SELECT status_online
        INTO @status
        FROM users
        WHERE id = user_id;

        IF @status = state THEN
            IF state = 1 THEN
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
