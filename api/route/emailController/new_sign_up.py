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

class MailHandlerClass:
  def __init__(self):
    pass

  def send_mail_setup(email, company_name, phone_number, full_name):
      app = Flask(__name__)
   
      mail_settings = {
            "MAIL_SERVER": 'smtp.gmail.com',
            "MAIL_PORT": 465,
            "MAIL_USE_TLS": False,
            "MAIL_USE_SSL": True,
            "MAIL_USERNAME": 'no-reply@africa118.com',
            "MAIL_PASSWORD": 'Resource2030'
            
            
      }
    

      app.config.update(mail_settings)

      subject = "New User SignUp"
      emailto = 'tbaraza@africa118.com'
      msg = Message(subject, sender = app.config.get('MAIL_USERNAME'), recipients = [emailto])
      msg.html=render_template("new_signup.html", email=email, company_name=company_name, phone_number=phone_number, full_name=full_name)
      

      try:
            with app.app_context():
                mail = Mail()
                mail.init_app(app)
                mail.send(msg)
            data = {'message': "success"}

      except Exception as e:
          data = {'message': str(e)}

      return data


def new_signup(email, company_name, phone_number, full_name):
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

    return MailHandlerClass.send_mail_setup(email, company_name, phone_number, full_name)