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

def hire_proffesional_client_email( email_address):
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

    subject = "Hire Professional"
    msg = Message(subject, sender = app.config.get('MAIL_USERNAME'), recipients = [emailto])
    msg.html=render_template("hire_professional_client.html")
    
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
