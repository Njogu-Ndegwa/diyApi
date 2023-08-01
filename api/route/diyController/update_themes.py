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

update_theme_api = Blueprint('update_theme_api', __name__)


@update_theme_api.route('/update-theme', methods=['GET'])
def update_themes():
    url = "https://api-sandbox.duda.co/api/sites/multiscreen/d57b6fbdd74f41e3b8308df2b5410359/theme"

    headers = {"accept": "application/json"}

    api_username = '29c00016'
    api_password = 'qqcylt5yOJow'

    payload = {
        
        "colors": [
        {
            "id": "color_1",
            "value": "#0000FF",
            "label": "Color"
        },
        {
            "id": "color_2",
            "value": "#0000FF",
            "label": "Color"
        },
        {
            "id": "color_3",
            "value": "#0000FF",
            "label": "Color"
        },
        {
            "id": "color_4",
            "value": "#0000FF",
            "label": "Color"
        },
        {
            "id": "color_5",
            "value": "#0000FF",
            "label": "Color"
        },
        {
            "id": "color_6",
            "value": "#0000FF",
            "label": "Color"
        },
                {
            "id": "color_7",
            "value": "#0000FF",
            "label": "Color"
        },
                {
            "id": "color_8",
            "value": "#0000FF",
            "label": "Color"
        }
    ]
    
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.put(
        url, json=payload, headers=headers, auth=(api_username, api_password))
    print(response, 'The Response')
    return response.text
