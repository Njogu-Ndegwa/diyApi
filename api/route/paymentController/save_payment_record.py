import datetime
import random
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
from api.route.configController.database import MySQLConnection
from api.route.emailController.finance_email import send_mail_finance



def save_payment_record(payment_amount, payment_method, email, customer_name):
   
   
    """
    login using provided username and passowrd
    ---
    tags:
      - login API endpoints
    parameters:
      - name: email
        in: query
        type: string
        required: true
        description: email parameter from user
      - name: password
        in: query
        type: string
        required: true
        description: password parameter from user
    responses:
      500:
        description: Error description!
      200:
        description: A user object based on login params
    """
    #query_param = request.args.get('query_string', default='', type=str)

    invoice_number = generate_ivoice()

    mysql_host =  os.environ.get('DB_HOST')
    mysql_user = os.environ.get('DB_USER')
    mysql_password = os.environ.get('DB_PASSWORD')
    mysql_database = os.environ.get('DB_DATABASE')
    # Database connection parameters

    try:
        conn = MySQLConnection(mysql_host, mysql_user, mysql_password, mysql_database)
        try:
            query_string = '''
                  INSERT INTO payments (invoice_number, payment_amount, payment_method, email) VALUES(%s, %s, %s, %s);
                               '''
            param = (invoice_number, payment_amount, payment_method, email)
            data = conn.query(query_string, param)
            send_mail_finance(customer_name, invoice_number, payment_amount, payment_method)
            print(data, 'Delete User')
            data = {
                'message': 'success'
            }
        except Exception as e:
            data = {'message': str(e)}

    except Exception as e:
        data = {'message': str(e)}

    return jsonify(data)


def generate_ivoice():
    # Get the current date and time down to the second
    now = datetime.datetime.now()
    formatted_date = now.strftime("%Y%m%d%H%M%S")

    # Generate a random incrementing number between 1 and 999 (you can adjust the range as needed)
    incrementing_number = random.randint(1, 999)

    # Create the invoice number
    invoice_number = f"INV-{formatted_date}-{incrementing_number:03d}"
    
    return invoice_number


