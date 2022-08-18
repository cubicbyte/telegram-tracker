/*DROP DATABASE IF EXISTS {db_name};*/

CREATE DATABASE IF NOT EXISTS {db_name};

USE {db_name};



CREATE TABLE IF NOT EXISTS statuses (
    Id BIGINT,
    UserStatus BOOLEAN,
    UpdateTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS users (
    Id BIGINT PRIMARY KEY,
    UserStatus BOOLEAN,
    UpdateTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    Expires DATETIME DEFAULT NULL
);



DROP PROCEDURE IF EXISTS updateUsers;
CREATE PROCEDURE updateUsers()
BEGIN

    INSERT INTO statuses
        (Id, UserStatus, UpdateTime)
    SELECT
        Id, 0, Expires
    FROM users
    WHERE
        Expires < CURRENT_TIMESTAMP;

    UPDATE users
    SET
        UserStatus = 0,
        UpdateTime = Expires,
        Expires = NULL
    WHERE
        Expires < CURRENT_TIMESTAMP;

END;



DROP PROCEDURE IF EXISTS setUserStatus;
CREATE PROCEDURE setUserStatus
(
    UserId BIGINT,
    UserStatusVar BOOLEAN,
    ExpiresVar DATETIME
)
BEGIN

    IF NOT EXISTS(SELECT * FROM users WHERE Id = UserId) THEN
        INSERT INTO users
            (Id, UserStatus, Expires)
        VALUES
            (UserId, UserStatusVar, IF(UserStatusVar, ExpiresVar, NULL));

        INSERT INTO statuses
            (Id, UserStatus)
        VALUES
            (UserId, UserStatusVar);

    ELSE

        SELECT 
            UserStatus, Expires
        INTO 
            @status, @expires
        FROM 
            users
        WHERE 
            Id = UserId;

        IF @status != UserStatusVar THEN
            UPDATE users
            SET
                UserStatus = UserStatusVar,
                Expires = IF(UserStatusVar, ExpiresVar, NULL),
                UpdateTime = CURRENT_TIMESTAMP
            WHERE
                Id = UserId;

            INSERT INTO statuses
                (Id, UserStatus)
            VALUES
                (UserId, UserStatusVar);

        ELSEIF @status = 1 AND @expires > CURRENT_TIMESTAMP THEN
            UPDATE users
            SET
                Expires = ExpiresVar
            WHERE
                Id = UserId;

        END IF;

    END IF;

END;



DROP FUNCTION IF EXISTS getUserOnlineCount;
CREATE FUNCTION getUserOnlineCount
(
    UserId BIGINT,
    FromDate DATETIME,
    ToDate DATETIME
)
RETURNS INT
READS SQL DATA
BEGIN

    DECLARE OnlineCount INT;

    SELECT
        COUNT(*)
    INTO
        OnlineCount
    FROM
        statuses
    WHERE
        UpdateTime BETWEEN FromDate AND ToDate
        AND Id = UserId
        AND UserStatus = 1;

    RETURN OnlineCount;

END;



DROP FUNCTION IF EXISTS getUserOnlineTime;
CREATE FUNCTION getUserOnlineTime
(
    UserId BIGINT,
    FromDate DATETIME,
    ToDate DATETIME
)
RETURNS INT
READS SQL DATA
BEGIN

    DECLARE OnlineTime INT DEFAULT 0;

    SELECT
        SUM(IF(OnlineTo IS NULL, OnlineFrom, OnlineTo) - OnlineFrom)
    INTO
        OnlineTime
    FROM (
        SELECT
            UpdateTime AS OnlineUpdateTime,
            UNIX_TIMESTAMP(UpdateTime) AS OnlineFrom,
            (
                SELECT
                    UNIX_TIMESTAMP(UpdateTime)
                FROM
                    statuses
                WHERE
                    Id = UserId
                    AND UpdateTime > OnlineUpdateTime
                    AND UserStatus = 0
                LIMIT 1
            ) AS OnlineTo
        FROM
            statuses
        WHERE
            Id = UserId
            AND UpdateTime BETWEEN FromDate AND ToDate
            AND UserStatus = 1
    ) AS T;

    RETURN OnlineTime;

END;



DROP PROCEDURE IF EXISTS getTopUsersOnlineCount;
CREATE PROCEDURE getTopUsersOnlineCount
(
    FromDate DATETIME,
    ToDate DATETIME
)
BEGIN
    
    SELECT
        Id, COUNT(Id) AS OnlineCount
    FROM
        (
            SELECT
                Id
            FROM
                statuses
            WHERE
                UpdateTime BETWEEN FromDate AND ToDate
                AND UserStatus = 1
        ) AS T
    GROUP BY
        Id
    ORDER BY
        OnlineCount DESC;

END;

