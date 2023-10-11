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
import jwt
from datetime import datetime, timedelta
from api.route.authController.acount_verification_token import generate_confirmation_token
from api.route.emailController.mail_handler_verify_account import send_account_verification_email
BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

resend_verification_email_api = Blueprint('resend_verification_email_api', __name__)

@resend_verification_email_api.route('/resend-verification-email', methods=['POST'])

def resend_verification_email():
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
    name = request.json.get('name')
    token = generate_confirmation_token(email)
    emailSend = send_account_verification_email(
            token, email, name)
    print(emailSend, 'Email...')
    data = {
        'message': 'success'
        }
    
    return jsonify(data)
