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
import os


BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

get_sites_api = Blueprint('get_sites_api', __name__)

@get_sites_api.route('/get-sites', methods=['POST'])

def get_sites():
    duda_endpoint = os.environ.get('DUDA_ENDPOINT')
    api_username = os.environ.get('DUDA_USERNAME')
    api_password = os.environ.get('DUDA_PASSWORD')
    site_name = request.json.get('site_name')
    url = f"{duda_endpoint}/sites/multiscreen/{site_name}"

    headers = {
        "accept": "application/json",
        "User-Agent": "Africa 118"
        }
    
    
    response = requests.get(url, headers=headers, auth=(api_username, api_password))
    print(response, '-----42----')
    print(response.json(), 'The JSON response')
    return response.json()