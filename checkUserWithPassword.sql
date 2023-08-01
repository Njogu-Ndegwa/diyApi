SELECT
    CASE
        WHEN count(*) = 0 THEN "User Not Found"
        ELSE "User Found"
    END AS user_status
FROM
    users
WHERE
    password = %s;