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
from api.route.emailController.mail_handler_verify_account import send_account_verification_email
# import quickemailverification
import mysql.connector

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

test_api = Blueprint('test_api', __name__)

@test_api.route('/test', methods=['GET'])
def test():
    data = {
        'data': 'Data'
    }

    return jsonify(data)
