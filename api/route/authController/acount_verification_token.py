import email
from itsdangerous import URLSafeTimedSerializer
import os
from http import HTTPStatus
from flask import Flask

# from flasgger import swag_from
from os.path import join
from pathlib import Path
from dotenv import load_dotenv
from passlib.apps import custom_app_context as pwd_context

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))



def generate_confirmation_token(email):


   app = Flask(__name__)
   app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET')
   app.config['SECURITY_PASSWORD_SALT'] =  os.environ.get('SECURITY_PASSWORD_SALT')


   

   serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    
   return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token,expiration=3600):
   app = Flask(__name__)
   app.config['SECRET_KEY'] = os.environ.get('JWT_SECRET')
   app.config['SECURITY_PASSWORD_SALT'] =  os.environ.get('SECURITY_PASSWORD_SALT')


   serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    
   try:
     email = serializer.loads(
        token,
        salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
          )
    
   except:
        return False
   return email    