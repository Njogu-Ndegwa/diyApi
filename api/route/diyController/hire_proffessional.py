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
from api.route.emailController.hire_professional_email import hire_proffesional_email
from api.route.emailController.hire_professional_client_email import hire_proffesional_client_email

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

hire_professional_api = Blueprint('hire_professional_api', __name__)

@hire_professional_api.route('/hire-professional', methods=['POST'])

def hire_proffesional():
    print('Hire Proffesional Called')
    full_name = request.json.get('full_name')
    email_address = request.json.get('email_address')
    phone_number = request.json.get('phone_number')
    communication_mode = request.json.get('communication_mode')
    assistance_type = request.json.get('assistance_type')
    other = request.json.get('other')
    
    data= {
        'full_name': full_name,
        'email_address': email_address,
        'phone_number': phone_number,
        'communication_mode': communication_mode,
        'assistance_type': assistance_type,
        'other': other
    }
    response = hire_proffesional_email(full_name, email_address, phone_number, communication_mode, other, assistance_type)
    print(response)
    hire_proffesional_client_email(email_address)
    return jsonify(data)