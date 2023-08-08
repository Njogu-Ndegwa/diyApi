UPDATE users
SET
    sso_link = %s
WHERE
    user_id = %s