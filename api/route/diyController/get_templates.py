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

get_templates_api = Blueprint('get_templates_api', __name__)

@get_templates_api.route('/get-templates', methods=['GET'])

def get_templates():
    template_url = "https://api-sandbox.duda.co/api/sites/multiscreen/templates"

    headers = {"accept": "application/json"}

    api_username = '29c00016'
    api_password = 'qqcylt5yOJow'


    response = requests.get(template_url, headers=headers, auth=(api_username, api_password))
    # print(response, 'The Response')
    return response.json()