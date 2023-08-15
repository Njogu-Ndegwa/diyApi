from os.path import join
from pathlib import Path
from flask import Flask, Blueprint
from dotenv import load_dotenv
import requests

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

verify_payment_api = Blueprint('verify_payment_api', __name__)

@verify_payment_api.route('/verify-payment', methods=['GET'])

def delete():
    url = "https://secure.3gdirectpay.com/API/v6/"
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml"
    }

    xml_data = '''
<?xml version="1.0" encoding="utf-8"?>
<API3G>
  <CompanyToken>8D3DA73D-9D7F-4E09-96D4-3D44E7A83EA3</CompanyToken>
  <Request>verifyToken</Request>
  <TransactionToken>FA4C76CC-5C3F-4873-AB73-B55D796AC585</TransactionToken>
</API3G>
    '''

    response = requests.post(url, headers=headers, data=xml_data)

    print(response.status_code)
    print(response.text)

