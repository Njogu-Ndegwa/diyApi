import os
import jwt
from datetime import datetime, timedelta
from functools import wraps
from http import HTTPStatus
from flask import Flask, Blueprint, jsonify, request, make_response, abort
# from flasgger import swag_from
from os.path import join
from pathlib import Path
from dotenv import load_dotenv
from passlib.apps import custom_app_context as pwd_context
from api.route.authController.acount_verification_token import generate_confirmation_token
from api.route.configController.mail_handler_verify_account import send_account_verification_email
# import quickemailverification
import mysql.connector
from api.route.configController.database import MySQLConnection
from werkzeug.security import generate_password_hash, check_password_hash

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

signup_api = Blueprint('signup_api', __name__)


@signup_api.route('/signup', methods=['POST'])
def signup():
    """
    signup using provided username and passowrd
    ---
    tags:
      - signup API endpoints
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
        description: A user object based on signup params
    """

    # Database connection parameters
    full_name = request.json.get('full_name')
    email = request.json.get('email')
    company = request.json.get('company', '')
    address = request.json.get('address', '')
    phone_number = request.json.get('phonenumber', '')
    # password = request.json.get('password')
    hashed_password = generate_password_hash(
        request.json.get('password'), method='sha256')
    db_config = {
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'database': os.environ.get('DB_DATABASE'),
    }
    mysql_host =  os.environ.get('DB_HOST')
    mysql_user = os.environ.get('DB_USER')
    mysql_password = os.environ.get('DB_PASSWORD')
    mysql_database = os.environ.get('DB_DATABASE')

    try:
        # conn = mysql.connector.connect(**db_config)
        conn = MySQLConnection(mysql_host, mysql_user, mysql_password, mysql_database)
        try:
            check_user_query = '''
                                  SELECT  CASE WHEN COUNT(*) = 0 THEN "User Not Found"  ELSE "User Found" END AS user_status
FROM users
WHERE email = %s;
                                '''
            param = (email,)
            print(email, 'Email....')
            check_user_result = conn.query(check_user_query, param)
            print(check_user_result, 'Check User Result')
            if check_user_result[0][0] != 'User Not Found':
                return make_response('A similar user already exists', 400)

            else:
                secret_key = os.environ.get('JWT_SECRET')
                api_token = secret_key

                # encoded = jwt.encode({'some': 'payload'}, 'secret', algorithm='HS256')

                token = jwt.encode({
                    'user': email,
                    # don't foget to wrap it in str function, otherwise it won't work [ i struggled with this one! ]
                    'expiration': str(datetime.utcnow() + timedelta(seconds=60))
                },
                    api_token
                )
                print(token, 'The token')

                # decoded_jwt = str(token.decode('utf-8'))
                decoded_jwt = str(token)

                hashed_password = str(hashed_password)
                # print(hashed_password)
                query_string = '''
                              INSERT INTO users (full_name, email, password, token) VALUES(%s, %s, %s, %s);
                              '''
                param = (full_name, email, hashed_password, decoded_jwt)

                data = conn.query(query_string, param)
                print(data, 'Sign Up Data---112---')
                
                token = generate_confirmation_token(email)
                # emailSend = send_account_verification_email(
                #     token, email, full_name)
                
                data = {
                    'success': 'success'
                }

        except Exception as e:
            data = {'message': str(e)}

    except Exception as e:
        data = {'message': str(e)}

    return jsonify(data)
