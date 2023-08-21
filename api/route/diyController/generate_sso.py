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

generate_sso_api = Blueprint('generate_sso_api', __name__)

@generate_sso_api.route('/generate-sso', methods=['POST'])

def generate_sso():
    account_name = request.json.get('account_name')
    site_name = request.json.get('site_name')
    sso_type = request.json.get('sso_type')

    print(sso_type, 'SSO type')
    print('Site Name', site_name)
    print(account_name, 'Account Name')
    url = f"https://api-sandbox.duda.co/api/accounts/sso/{account_name}/link?site_name={site_name}&target={sso_type}"

    headers = {"accept": "application/json"}

    api_username = '29c00016'
    api_password = 'qqcylt5yOJow'

    auth=(api_username, api_password)

    response = requests.get(url, headers=headers, auth=auth)
    print(response.json(), 'The Response')
    json_response = response.json()
    sso_link = json_response['url']
    data = {
                "sso_link": sso_link
            }
    
    return jsonify(data)