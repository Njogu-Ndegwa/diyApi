UPDATE users
SET 
    full_name = %s,
    email = %s,
    phone_number = %s,
    business_email = %s,
    business_phone_number = %s,
    company_name = %s,
    profile_url = %s
WHERE
    user_id = %s