import os
from http import HTTPStatus
from os.path import join
from pathlib import Path

from dotenv import load_dotenv
# from flasgger import swag_from
from flask import Blueprint, jsonify, make_response, request, abort
from passlib.apps import custom_app_context as pwd_context
from werkzeug.security import check_password_hash, generate_password_hash
# import quickemailverification
import mysql.connector
from api.route.configController.database import MySQLConnection


BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

login_api = Blueprint('login_api', __name__)

@login_api.route('/login', methods=['POST'])

def login():
    """
    login using provided username and passowrd
    ---
    tags:
      - login API endpoints
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
        description: A user object based on login params
    """
    #query_param = request.args.get('query_string', default='', type=str)
    email = request.json.get('email')
    phone_number= request.json.get('phone_number')
    password_str = request.json.get('password')

    mysql_host =  os.environ.get('DB_HOST')
    mysql_user = os.environ.get('DB_USER')
    mysql_password = os.environ.get('DB_PASSWORD')
    mysql_database = os.environ.get('DB_DATABASE')
    # Database connection parameters

    try:
        conn = MySQLConnection(mysql_host, mysql_user, mysql_password, mysql_database)
        print(conn, 'Print the Connection')
        try:
            check_user_password = '''
                        SELECT 
                            password
                        FROM
                            users
                        WHERE email = %s;
                               '''
            param = (email,)
            user_password_result = conn.query(check_user_password, param)
            print(user_password_result, 'User Password Result')
            hashed_password = str(user_password_result[0][0])
            print(hashed_password, 'The Hashed password')
            # print(password_str, 'Password')
            # print('-------74-------')
            # print(check_password_hash(hashed_password, password_str), 'Check Password Hash')
            if len(user_password_result) > 0 and user_password_result[0][0]:
              hashed_password = str(user_password_result[0][0])
              print(check_password_hash(hashed_password, password_str), 'Check Password Hash')
              if check_password_hash(hashed_password, password_str):
                # print(password_str)
                query_string = '''
                SELECT 
                    *
                FROM 
                    users
                WHERE
                    email = %s AND password = %s;
                                '''
                
                param = (email, hashed_password)
                data = conn.query(query_string, param)
                print(data, 'Data--92---')
                formatted_result = []
                for row in data:
                    data = {
                        'id': row[0],
                        'email': row[1],
                        'token': row[5],
                        'full_name': row[6],
                        'account_name': row[8],
                        'site_name':row[9],
                        'template_id':row[10]
                        
                    }
                    formatted_result.append(data)
                data = formatted_result
                # print(formatted_result)

    
              else:
                return make_response('Password mismatch', 400)
            else:  
              return make_response('Incorrect username or password', 400)
        except Exception as e:
            return make_response('User not Found', 404)

    except Exception as e:
        data = {'message': str(e)}

    return jsonify(data)
