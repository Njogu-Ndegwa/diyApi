from os.path import join
from pathlib import Path
from flask import Flask, Blueprint, request, jsonify
from dotenv import load_dotenv
import requests
import xml.etree.ElementTree as ET
from api.route.paymentController.save_payment_record import save_payment_record

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

verify_payment_api = Blueprint('verify_payment_api', __name__)

@verify_payment_api.route('/verify-payment', methods=['POST'])

def verify_payment():
    email = request.json.get('email')
    transaction_token = request.json.get('transaction_token')
    url = "https://secure.3gdirectpay.com/API/v6/"
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml"
    }

    xml_data = f'''
<?xml version="1.0" encoding="utf-8"?>
<API3G>
  <CompanyToken>02900042-8063-4C63-9B45-EFA4333C73EF</CompanyToken>
  <Request>verifyToken</Request>
  <TransactionToken>{transaction_token}</TransactionToken>
</API3G>
    '''

    response = requests.post(url, headers=headers, data=xml_data)

    # print(response.status_code)
    print(response.text)
    # Parse the XML content

    root = ET.fromstring(response.text)

    # Find the MobilePaymentRequest element
    mobile_payment_request = root.find(".//MobilePaymentRequest")
    transaction_amount_request = root.find(".//TransactionFinalAmount")
    transaction_status_request = root.find(".//Result")
    customer_name_request = root.find(".//CustomerName")


    if customer_name_request is not None:
        customer_name = customer_name_request.text
    else:
        customer_name = ''
    # print(transaction_status, 'Transaction Status')

    if mobile_payment_request is not None:
        print('--------57---------')
        mobile_payment_status = mobile_payment_request.text
        transaction_amount = transaction_amount_request.text
        transaction_status = transaction_status_request.text
        
        print('-------62------')
        if mobile_payment_status == 'Paid':
            print(customer_name, 'Customer Name')
            save_payment_record(transaction_amount, 'MPESA', email, customer_name)
            data = {
                'status': 'paid',
                'amount': transaction_amount
            }
            return jsonify(data)

        elif transaction_status == '000':
            save_payment_record(transaction_amount, 'CARD', email, customer_name)
            data = {
                'status': 'paid',
                'amount': transaction_amount
            }
            return jsonify(data)
        else:
            data = {
                'status': 'failed' 
            }
            return jsonify(data)
    else:
        data = {
            'status': 'failed'
        }
        return jsonify(data)


