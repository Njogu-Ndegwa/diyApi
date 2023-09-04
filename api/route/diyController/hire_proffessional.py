import requests
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


BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

hire_professional_api = Blueprint('hire_professional_api', __name__)

@hire_professional_api.route('/hire-professional', methods=['POST'])

def hire_proffesional():
    full_name = request.json.get('full_name')
    email_address = request.json.get('email_address')
    phone_number = request.json.get('phone_number')
    communication_mode = request.json.get('communication_mode')
    others = request.json.get('others')
    pass