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
import base64
import datetime
import uuid

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

get_profile_api = Blueprint('get_profile_api', __name__)

@get_profile_api.route('/get-profile', methods=['POST'])

def get_profile():
    """
    add the profile
    ---
    tags:
      - profile API endpoints
    parameters:
      - user_id: User id
        in: user_id
        type: string
        required: true
        description: name parameter from user

    responses:
      500:
        description: Error description!
      200:
        description: A user object based on login params
    """

    user_id = request.json.get('user_id')

    mysql_host =  os.environ.get('DB_HOST')
    mysql_user = os.environ.get('DB_USER')
    mysql_password = os.environ.get('DB_PASSWORD')
    mysql_database = os.environ.get('DB_DATABASE')
    # Database connection parameters

    try:
        conn = MySQLConnection(mysql_host, mysql_user, mysql_password, mysql_database)
        try:
            query_string = '''
SELECT * FROM users

WHERE
    user_id = %s
                               '''
            param = (user_id,)
            data = conn.query(query_string, param)
            formatted_result = []
            for row in data:
              data = {
                  'message': 'success',
                  'email': row[1],
                  'company_name': row[2],
                  'business_phone_number': row[4],
                  'business_email': row[12],
                  'full_name':row[6],
                  'photo_url': row[14],
                  'phone_number': row[13]
              }
              formatted_result.append(data)
            data  = formatted_result
        except Exception as e:
            data = {'message': str(e)}

    except Exception as e:
        data = {'message': str(e)}

    return jsonify(data)
