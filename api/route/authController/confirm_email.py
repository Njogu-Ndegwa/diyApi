import os
from http import HTTPStatus
from os.path import join
from pathlib import Path

from api.route.authController.acount_verification_token import confirm_token
from dotenv import load_dotenv
# from flasgger import swag_from
from flask import Blueprint, jsonify, make_response, redirect, request
from passlib.apps import custom_app_context as pwd_context
from api.route.configController.database import MySQLConnection

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

confirmAccount_api = Blueprint('confirmAccount_api', __name__)

@confirmAccount_api.route('/confirm/<token>', methods=['GET'])

def confirmAccount(token):
    """
    confirmAccount using provided username and passowrd
    ---
    tags:
      - confirmAccount API endpoints
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: email parameter from user
      - name: password
        in: query
        type: string
        required: true
        description: password parameter from user
    responses:
      500:
        description: Error description!
      200:
        description: A user object based on confirmAccount params
    """

    # Database connection parameters
    mysql_host =  os.environ.get('DB_HOST')
    mysql_user = os.environ.get('DB_USER')
    mysql_password = os.environ.get('DB_PASSWORD')
    mysql_database = os.environ.get('DB_DATABASE')

    try:
        email_var = confirm_token(token)
        print(email_var, 'Email Variable---53')
    except:
        return make_response( 'The confirmation link is invalid or has expired.', 400)

    try:
        conn = MySQLConnection(mysql_host, mysql_user, mysql_password, mysql_database)
        try:
            check_user_query = '''
SELECT email_verification_status FROM users WHERE email = %s
                                '''
            param = (email_var,)
            check_user_result = conn.query(check_user_query, param)
            print(check_user_result, '----65---')
            if check_user_result[0] == True:
              return redirect('https://diy.infomoby.com/account-verification-status-warning')

            else:  
              print('----70----')
              query_string = '''
UPDATE users
SET
    email_verification_status =  True
WHERE
    email = %s
                              '''

              param = (email_var,)
              data = conn.query(query_string, param)
              print(data, '------81-----')
              return redirect('https://diy.infomoby.com/account-verification-status-success')
 
        except Exception as e:
            data = {'message': str(e)}

    except Exception as e:
        data = {'message': str(e)}

    return redirect('https://diy.infomoby.com/login')


