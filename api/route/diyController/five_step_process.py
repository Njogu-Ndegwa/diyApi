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
from api.route.diyController.save_account_and_site import save_accountname_sitename
duda_endpoint = os.environ.get('DUDA_ENDPOINT')

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

five_step_process_api = Blueprint('five_step_process_api', __name__)

@five_step_process_api.route('/five-step-process', methods=['POST'])

def diyapis():
    business_name = request.json.get('business_name')
    template_id = request.json.get('template_id')
    person_object = request.json.get('person_object')
    user_id = request.json.get('user_id')
    account_name = person_object['email']
    business_phone = request.json.get('business_phone_number')
    business_email = request.json.get('business_email')

    api_username = os.environ.get('DUDA_USERNAME')
    api_password = os.environ.get('DUDA_PASSWORD')
    auth=(api_username, api_password)
    site_name = create_website(auth, business_name, business_phone, business_email)
    site_id_update_response = update_site_planid(auth, site_name)
    if site_id_update_response == 200:
        pass
    else:
        return make_response('There was a problem creating the site', 400)
    create_user_status_code = create_user(auth, person_object)
    if create_user_status_code == 204:
        assign_permissions_reponse_code = assign_permissions(auth, account_name, site_name)
        if assign_permissions_reponse_code ==  204:
            sso_link = generate_sso_link(auth, account_name, site_name)
            data = {
                "account_name": account_name,
                "site_name":site_name,
                "sso_link": sso_link

            }
            res = save_accountname_sitename(account_name, site_name, template_id, user_id)
            return jsonify(data)
        else:
            return make_response('Permissions not assigned',  400)
    else:
        return make_response('Client already exists in the Database', 400)

def create_website(auth, business_name, business_phone, business_email):
    url = f"{duda_endpoint}/sites/multiscreen/create"

    data = {
            'template_id': '1000440',
             "site_data": { "site_business_info": {  
                "email": business_email,
                "phone_number": business_phone,
                "business_name": business_name 
                } } ,        
        }
    
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "User-Agent": "Africa 118"
    }

    response = requests.post(url, headers=headers, json=data, auth=auth)
    json_response = response.json()
    return json_response['site_name']


def update_site_planid(auth, site_name):
    url = f"{duda_endpoint}/sites/multiscreen/{site_name}/plan/800"
    headers = {
        "accept": "application/json",
        "User-Agent": "Africa 118"
        }
    response = requests.post(url, headers=headers, auth=auth)
    print(response.status_code, "-Status Code of the Response---90--")
    if response.status_code == 204:
        return 200
    else:
        return 500


def create_user(auth, person_object):
    account_name = person_object['email']
    first_name = person_object['first_name']
    email = person_object['email']
    phone = person_object['phone']

    url = f"{duda_endpoint}/accounts/create"
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "User-Agent": "Africa 118"
    }

    payload = {
    "account_name": account_name,
    "first_name": first_name,
    "email": email
    }

    response = requests.post(url, json=payload, headers=headers, auth=auth)
    return response.status_code

def assign_permissions(auth, account_name, site_name):
    url = f"{duda_endpoint}/accounts/{account_name}/sites/{site_name}/permissions"
    payload = { "permissions": ["PUSH_NOTIFICATIONS", "REPUBLISH", "EDIT", "INSITE", "PUBLISH", "CUSTOM_DOMAIN", "RESET", "SEO", "STATS_TAB", "BLOG"] }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "User-Agent": "Africa 118"
    }

    response = requests.post(url, headers=headers, json=payload, auth=auth)
    assign_permissions_reponse_code = response.status_code
    return assign_permissions_reponse_code


def generate_sso_link(auth, account_name, site_name):
    url = f"{duda_endpoint}/accounts/sso/{account_name}/link?site_name={site_name}&target=RESET_BASIC"
    headers = {
        "accept": "application/json",
        "User-Agent": "Africa 118"
        }

    response = requests.get(url, headers=headers, auth=auth)

    json_response = response.json()
    return json_response['url']
