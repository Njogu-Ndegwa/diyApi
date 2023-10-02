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

profile_api = Blueprint('profile_api', __name__)

@profile_api.route('/user-profile', methods=['GET'])

def profile():
    """
    add the profile
    ---
    tags:
      - profile API endpoints
    parameters:
      - name: name
        in: query
        type: string
        required: true
        description: name parameter from user
      - name: Email Address
        in: email_address
        type: string
        required: false
        description: Email Address parameter from user
      - name: Phone Number
        in: phone_number
        type: string
        required: false
        description: Phone Number parameter from user
      - name: Photo
        in: photo
        type: string
        required: false
        description: Photo parameter from user
      - name: Business Name
        in: business_name
        type: string
        required: false
        description: Business Name parameter from user
      - name: Business Email
        in: business_email
        type: string
        required: false
        description: Business Email parameter from user
      - name: Business Phone Number
        in: business_phone_number
        type: string
        required: false
        description: Business Phone Number parameter from user
    responses:
      500:
        description: Error description!
      200:
        description: A user object based on login params
    """
    #query_param = request.args.get('query_string', default='', type=str)
    name = request.json.get('name')
    email_address = request.json.get('email_address')
    photo = request.json.get('photo')
    business_name = request.json.get('business_name')
    business_email = request.json.get('business_email')
    business_phone_number = request.json.get('business_phone_number')

    mysql_host =  os.environ.get('DB_HOST')
    mysql_user = os.environ.get('DB_USER')
    mysql_password = os.environ.get('DB_PASSWORD')
    mysql_database = os.environ.get('DB_DATABASE')
    # Database connection parameters

    try:
        conn = MySQLConnection(mysql_host, mysql_user, mysql_password, mysql_database)
        try:
            query_string = '''
                  DELETE FROM users WHERE email = %s
                               '''
            param = (email,)
            data = conn.query(query_string, param)
            print(data, 'Delete User')

        except Exception as e:
            data = {'message': str(e)}

    except Exception as e:
        data = {'message': str(e)}

    return jsonify(data)
