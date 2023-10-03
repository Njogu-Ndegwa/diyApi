import os
from http import HTTPStatus
from os.path import join
from pathlib import Path

from dotenv import load_dotenv
# from flasgger import swag_from
from flask import Blueprint, jsonify, make_response, request, abort, send_from_directory
from passlib.apps import custom_app_context as pwd_context
from werkzeug.security import check_password_hash, generate_password_hash
# import quickemailverification
import mysql.connector
from api.route.configController.database import MySQLConnection
import random
from api.route.emailController.reset_password_email import send_reset_password_email

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

serve_uploads_api = Blueprint('serve_uploads_api', __name__)

@serve_uploads_api.route('/uploads/<filename>', methods=['get'])

def serve_uploads(filename):
    """
    reset password from this email
    ---
    tags:
      - reset password API endpoints
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: email parameter from user
    responses:
      500:
        description: Error description!
      200:
        description: Password reset Succesfully
    """
    return send_from_directory('uploads', filename)
        

