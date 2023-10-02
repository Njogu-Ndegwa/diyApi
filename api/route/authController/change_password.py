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
from api.route.configController.database import MySQLConnection
import random
from api.route.emailController.reset_password_email import send_reset_password_email

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

change_password_api = Blueprint('change_password_api', __name__)

@change_password_api.route('/change-password', methods=['POST'])

def change_password():
    """
    change password from this email
    ---
    tags:
      - change password API endpoints
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: email parameter from user
    - name: password1
        in: query
        type: string
        required: true
        description: password1 parameter from user
    - name: password2
        in: query
        type: string
        required: true
        description: password2 parameter from user
    responses:
      500:
        description: Error description!
      200:
        description: Password reset Succesfully
    """
    #query_param = request.args.get('query_string', default='', type=str)
    email = request.json.get('email')
    password = request.json.get('password1')
    hashed_password = generate_password_hash(
        password, method='sha256')



    mysql_host =  os.environ.get('DB_HOST')
    mysql_user = os.environ.get('DB_USER')
    mysql_password = os.environ.get('DB_PASSWORD')
    mysql_database = os.environ.get('DB_DATABASE')
    # Database connection parameters
    # This will be inserting a Verification code to the user object. 
    try:
        conn = MySQLConnection(mysql_host, mysql_user, mysql_password, mysql_database)
        try:
            query_string = '''
                 UPDATE users
SET password = %s
WHERE email = %s


                               '''
            param = (hashed_password, email)
            data = conn.query(query_string, param)
            print(data, 'The Change Password Result')
            data = {
                'message':'success'
            }

        except Exception as e:
            data = {'message': str(e)}

    except Exception as e:
        data = {'message': str(e)}

    return jsonify(data)
