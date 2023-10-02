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

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

confirm_verification_code_api = Blueprint('confirm_verification_code_api', __name__)

@confirm_verification_code_api.route('/confirm-verification-code', methods=['POST'])

def confirm_verification_code():
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
    verification_code = request.json.get('verification_code')

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
            stored_code = verification_code
            if verification_code == stored_code:
                data = {
                    'message':'success'
                }

            else:
                data = {
                    'message':'error'
                }

        except Exception as e:
            data = {'message': str(e)}

    except Exception as e:
        data = {'message': str(e)}

    return jsonify(data)
