UPDATE users
SET 
    verification_code =  %s
WHERE
    user_id = %s