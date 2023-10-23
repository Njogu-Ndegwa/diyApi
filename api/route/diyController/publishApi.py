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

publish_site_api = Blueprint('publish_site_api', __name__)

@publish_site_api.route('/publish-site', methods=['POST'])

def publish_site():
    site_name = request.json.get('site_name')
    site_name = site_name.rstrip()
    print(site_name)
    domain = request.json.get('domain')
    duda_endpoint = os.environ.get('DUDA_ENDPOINT')
    api_username = os.environ.get('DUDA_USERNAME')
    api_password = os.environ.get('DUDA_PASSWORD')
    url = f"{duda_endpoint}/sites/multiscreen/publish/{site_name}"
    print(url, 'Ur---30')
    print(domain, 'The Domain')
    # url = "https://api.eu.duda.co/api/sites/multiscreen/publish/b22a80065f39432aa9d9c1f60cfa23ca"

    headers = {
        "accept": "application/json",
        "User-Agent": "Africa 118"
        }

    response = requests.post(url, headers=headers, auth=(api_username, api_password))
    print(response, 'The Response')
    payload = { "site_domain": domain }
    if response.status_code == 204:
        update_url = f"{duda_endpoint}/sites/multiscreen/update/{site_name}"
        print(update_url, '----44---')
        response = requests.post(update_url, json=payload, headers=headers, auth=(api_username, api_password))
        print('---------------------')
        print(response, flush=True)
        print('---------------------')
        if response.status_code == 204:
            data = {
                'message': 'success'
            }
            return jsonify(data)
        else:
            data = {
                'message': 'error'
            } 
            return jsonify(data)
        
    else:
        data = {
                'message': 'error'
            } 
        return jsonify(data)