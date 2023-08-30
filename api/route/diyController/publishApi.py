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
    domain = request.json.get('domain')
    url = f"https://api-sandbox.duda.co/api/sites/multiscreen/publish/{site_name}"

    headers = {"accept": "application/json"}

    api_username = '29c00016'
    api_password = 'qqcylt5yOJow'

    response = requests.get(url, headers=headers, auth=(api_username, api_password))

    json_response = response.json()
    payload = { "site_domain": domain }
    if json_response.response_code == 204:
        update_url = f"https://api-sandbox.duda.co/api/sites/multiscreen/update/{site_name}"
        response = requests.get(update_url, json=payload, headers=headers, auth=(api_username, api_password))
        json_response = response.json()
        if json_response.response_code == 204:
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