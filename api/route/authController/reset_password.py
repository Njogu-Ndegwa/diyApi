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
import random
from api.route.emailController.reset_password_email import send_reset_password_email

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

reset_password_api = Blueprint('reset_password_api', __name__)

@reset_password_api.route('/reset-password', methods=['POST'])

def reset_password():
    """
    reset password from this email
    ---
    tags:
      - reset password API endpoints
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: email parameter from user
    responses:
      500:
        description: Error description!
      200:
        description: Password reset Succesfully
    """
    #query_param = request.args.get('query_string', default='', type=str)
    email = request.json.get('email')
    six_digit_code = random.randint(100000, 999999)

    mysql_host =  os.environ.get('DB_HOST')
    mysql_user = os.environ.get('DB_USER')
    mysql_password = os.environ.get('DB_PASSWORD')
    mysql_database = os.environ.get('DB_DATABASE')
    # Database connection parameters
    # This will be inserting a Verification code to the user object. 
    try:
        conn = MySQLConnection(mysql_host, mysql_user, mysql_password, mysql_database)
        try:
            # query_string = '''
            #       DELETE FROM users WHERE email = %s
            #                    '''
            # param = (email, six_digit_code)
            # data = conn.query(query_string, param)
            send_reset_password_email(email, six_digit_code)
            data = {
                'message':'success'
            }

        except Exception as e:
            data = {'message': str(e)}

    except Exception as e:
        data = {'message': str(e)}

    return jsonify(data)
