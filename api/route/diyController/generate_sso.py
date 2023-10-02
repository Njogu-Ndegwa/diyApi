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
    duda_endpoint = os.environ.get('DUDA_ENDPOINT')
    api_username = os.environ.get('DUDA_USERNAME')
    api_password = os.environ.get('DUDA_PASSWORD')
    url = f"{duda_endpoint}/accounts/sso/{account_name}/link?site_name={site_name}&target={sso_type}"

    headers = {
        "accept": "application/json",
        "User-Agent": "Africa 118"
        }

    auth=(api_username, api_password)

    response = requests.get(url, headers=headers, auth=auth)
    json_response = response.json()
    sso_link = json_response['url']
    data = {
                "sso_link": sso_link
            }
    
    return jsonify(data)