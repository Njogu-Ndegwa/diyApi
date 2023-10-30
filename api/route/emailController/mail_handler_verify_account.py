import os
from http import HTTPStatus
from os.path import join
from pathlib import Path

from dotenv import load_dotenv
from flask import (Blueprint, Flask, make_response, render_template, request,
                   url_for)
from flask_mail import Mail, Message
from passlib.apps import custom_app_context as pwd_context
from werkzeug.security import check_password_hash, generate_password_hash


BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

class MailHandlerClass:
  def __init__(self, user_id):
      self.__user_id = user_id

  def send_mail_setup(token, recepientEmail,recipientName):
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
      confirm_url = url_for('confirmAccount_api.confirmAccount', token=token, _external=True, _scheme='https')

      subject = "Please Confirm Your Email Address" 
      msg = Message(subject, sender = app.config.get('MAIL_USERNAME'), recipients = [recepientEmail])
      msg.html=render_template("verify_user_account.html",confirm_url = confirm_url,name=recipientName)


      try:
            with app.app_context():
                mail = Mail()
                mail.init_app(app)
                mail.send(msg)
            data = {'message': str("Email sent")}
            

      except Exception as e:
          data = {'message': str(e)}

      return data


def send_account_verification_email(token,recepientEmail,recipientName):
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


    return MailHandlerClass.send_mail_setup(token, recepientEmail,recipientName)