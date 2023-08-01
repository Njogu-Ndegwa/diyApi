SELECT 
    *
FROM 
    users
WHERE
    email = %s AND password = %s;
