import os
from http import HTTPStatus
from os.path import join
from pathlib import Path

from dotenv import load_dotenv
# from flasgger import swag_from
from flask import (Blueprint, Flask, jsonify, make_response, render_template,
                   request)
from flask_mail import Mail, Message
from passlib.apps import custom_app_context as pwd_context
from werkzeug.security import check_password_hash, generate_password_hash


BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

# class MailHandlerClass:
#   def __init__(self):
#     pass

def hire_proffesional_email(full_name, email_address, phone_number, communication_mode, others, assistance_type):
    app = Flask(__name__)

    mail_settings = {
        "MAIL_SERVER": 'smtp.gmail.com',
        "MAIL_PORT": 465,
        "MAIL_USE_TLS": False,
        "MAIL_USE_SSL": True,
        "MAIL_USERNAME": 'no-reply@africa118.com',
        "MAIL_PASSWORD": 'Resource2030'
        
        
        
        
        # "MAIL_SERVER": 'smtp.mandrillapp.com',
        # "MAIL_PORT": 587,
        # "MAIL_USE_TLS": True,
        # "MAIL_USE_SSL": False,
        # "MAIL_USERNAME": 'markgichohi24@',
        # "MAIL_PASSWORD": 'RNRFUgJwZPeJBAbrX3XwAA'
    }
    emailto = email_address

    app.config.update(mail_settings)

    subject = "Hire Proffessional" 
    msg = Message(subject, sender = app.config.get('MAIL_USERNAME'), recipients = [emailto])
    msg.html=render_template("hire_professional.html", full_name=full_name, email_address=email_address, phone_number=phone_number, communication_mode=communication_mode, others=others, assistance_type=assistance_type)
    
    # return render_template("home.html", confirm_msg=confirm_msg)


    # msg.body = emailContent

    try:
        with app.app_context():
            mail = Mail()
            mail.init_app(app)
            mail.send(msg)
        data = {'message': str("Email sent")}

    except Exception as e:
        data = {'message': str(e)}

    return data

send_mail_finance_api = Blueprint('send_mail_finance_api', __name__)

@send_mail_finance_api.route('/send_mail_finance', methods=['POST'])

def send_mail_finance():
    """
    fetchemployees with various available filters
    ---
    tags:
      - fetchemployees API endpoints
    parameters:
      - name: query_string
        in: query
        type: string
        required: false
        description: any fetchemployees parameter from database
      - name: start
        in: query
        type: int
        required: false
        description: any fetchdecisionmakerbyid parameter from user
      - name: offset
        in: query
        type: int
        required: false
        description: any fetchdecisionmakerbyid parameter from user
    responses:
      500:
        description: Error description!
      200:
        description: A list of employees based on fetchemployees params
    """
    emailto = request.json.get('emailto')
    # emailFrom = request.json.get('emailfrom')
    # senderName = request.json.get('name')
    # message = request.json.get('message')

    return MailHandlerClass.send_mail_setup(emailto)