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

five_step_process_api = Blueprint('five_step_process_api', __name__)

@five_step_process_api.route('/five-step-process', methods=['POST'])

def diyapis():
    business_name = request.json.get('business_name')
    template_id = request.json.get('template_id')
    email = request.json.get('email')
    account_name = email
    phone_number = request.json.get('phone_number')
    first_name = request.json.get('full_name')
    person_object = request.json.get('person_object')
    api_username = '29c00016'
    api_password = 'qqcylt5yOJow'

    auth=(api_username, api_password)

    site_name = create_website(auth, business_name, template_id)
    create_user_status_code = create_user(auth, person_object)
    if create_user_status_code == 204:
        assign_permissions_reponse_code = assign_permissions(auth, account_name, site_name)
        if assign_permissions_reponse_code ==  204:
            sso_link = generate_sso_link(auth, account_name, site_name)
            data = {
                "sso_link": sso_link
            }

            return jsonify(data)
        else:
            pass
    else:
        pass

def create_website(auth, business_name, template_id):
    print('Create Website')
    url = "https://api-sandbox.duda.co/api/sites/multiscreen/create"

    data = {
            'template_id': template_id,
             "site_data": { "site_business_info": { "business_name": business_name } }          
        }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "User-Agent": "User Agent"
    }

    response = requests.post(url, headers=headers, json=data, auth=auth)

    json_response = response.json()
    return json_response['site_name']


def create_user(auth, person_object):
    print('Create User')
    account_name = person_object['email']
    first_name = person_object['first_name']
    email = person_object['email']
    phone = person_object['phone']
    url = "https://api-sandbox.duda.co/api/accounts/create"

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    payload = {
    "account_name": account_name,
    "first_name": first_name,
    "email": email
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    # print(response, 'Response')
    return response.status_code

def assign_permissions(auth, account_name, site_name):
    print('Assign Permissions')
    url = "https://api-sandbox.duda.co/api/accounts/dennisndegwa57%40gmail.com/sites/d57b6fbdd74f41e3b8308df2b5410359/permissions"

    payload = { "permissions": ["PUSH_NOTIFICATIONS", "REPUBLISH", "EDIT", "INSITE", "PUBLISH", "CUSTOM_DOMAIN", "RESET", "SEO", "STATS_TAB", "BLOG"] }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload, auth=auth)

    assign_permissions_reponse_code = response.status_code

    return assign_permissions_reponse_code


def generate_sso_link(auth, account_name, site_name):
    print('Generate SSO Link')
    url = "https://api-sandbox.duda.co/api/accounts/sso/dennisndegwa57%40gmail.com/link?site_name=d57b6fbdd74f41e3b8308df2b5410359"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers, auth=auth)

    # print(response, 'Response, ----114----')
    json_response = response.json()
    return json_response['url']
