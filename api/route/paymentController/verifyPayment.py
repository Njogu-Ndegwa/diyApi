from os.path import join
from pathlib import Path
from flask import Flask, Blueprint, request, jsonify
from dotenv import load_dotenv
import requests
import xml.etree.ElementTree as ET
BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

verify_payment_api = Blueprint('verify_payment_api', __name__)

@verify_payment_api.route('/verify-payment', methods=['POST'])

def verify_payment():

    transaction_token = request.json.get('transaction_token')
    url = "https://secure.3gdirectpay.com/API/v6/"
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml"
    }

    xml_data = f'''
<?xml version="1.0" encoding="utf-8"?>
<API3G>
  <CompanyToken>8D3DA73D-9D7F-4E09-96D4-3D44E7A83EA3</CompanyToken>
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

    # print(transaction_status, 'Transaction Status')
    if mobile_payment_request is not None:
        mobile_payment_status = mobile_payment_request.text
        transaction_amount = transaction_amount_request.text
        transaction_status = transaction_status_request.text
        print(transaction_status, 'Status')
        print(mobile_payment_status, transaction_amount, '-------46-----', flush=True)
        if mobile_payment_status == 'Paid':
            data = {
                'status': 'paid',
                'amount': transaction_amount
            }
            return jsonify(data)

        elif transaction_status == '000':
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
        print("Mobile Payment Request element not found.")
