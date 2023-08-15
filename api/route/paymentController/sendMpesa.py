from os.path import join
from pathlib import Path
from flask import Flask, Blueprint, request, jsonify
from dotenv import load_dotenv
import requests

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

send_mpesa_api = Blueprint('send_mpesa_api', __name__)

@send_mpesa_api.route('/send-mpesa', methods=['POST'])

def send_mpesa():
    transaction_token = request.json.get('trans_token')
    phonenumber = request.json.get('phonenumber')

    url = "https://secure.3gdirectpay.com/API/v6/"
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml"
    }

    xml_data = f'''
<?xml version="1.0" encoding="UTF-8"?>
<API3G>
  <CompanyToken>8D3DA73D-9D7F-4E09-96D4-3D44E7A83EA3</CompanyToken>
  <Request>ChargeTokenMobile</Request>
  <TransactionToken>{transaction_token}</TransactionToken>
  <PhoneNumber>{phonenumber}</PhoneNumber>
  <MNO>mpesa</MNO>
  <MNOcountry>kenya</MNOcountry>
</API3G>
    '''

    response = requests.post(url, headers=headers, data=xml_data)

    print(response.status_code)
    print(response.text)

    data = {
        'success': 'success'
    }

    return jsonify(data)
