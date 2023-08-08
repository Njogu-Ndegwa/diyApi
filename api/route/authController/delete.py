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

delete_api = Blueprint('delete_api', __name__)

@delete_api.route('/delete', methods=['GET'])

def delete():
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
