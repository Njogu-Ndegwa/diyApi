UPDATE users
SET
    site_name = %s,
    account_name = %s
WHERE
    user_id = %s