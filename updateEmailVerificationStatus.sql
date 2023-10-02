UPDATE users
SET 
    email_verification_status =  %s
WHERE
    user_id = %s