from os.path import join
from pathlib import Path
from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

payment_api = Blueprint('payment_api', __name__)

@payment_api.route('/payment', methods=['POST'])

def create_token():

    payment_amount = request.json.get('amount')

    url = "https://secure.3gdirectpay.com/API/v6/"
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml"
    }

    current_date = datetime.now()
    xml_data = f'''<?xml version='1.0' encoding='utf-8'?>
    <API3G>
        <CompanyToken>02900042-8063-4C63-9B45-EFA4333C73EF</CompanyToken>
        <Request>createToken</Request>
        <Transaction>
            <PaymentAmount>{payment_amount}</PaymentAmount>
            <PaymentCurrency>KES</PaymentCurrency>
            <CompanyRef>49FKEOA</CompanyRef>
            <RedirectURL>https://diy.infomoby.com/verify-payment</RedirectURL>
            <BackURL>https://diy.infomoby.com/payment</BackURL>
            <CompanyRefUnique>0</CompanyRefUnique>
            <PTL>5</PTL>
        </Transaction>
        <Services>
            <Service>
                <ServiceType>81237</ServiceType>
                <ServiceDescription>Payment for DIY</ServiceDescription>
                <ServiceDate>{current_date}</ServiceDate>
            </Service>
        </Services>
    </API3G>
    '''

    response = requests.post(url, headers=headers, data=xml_data)
    print(response.status_code, '49---------------')
    print(response.text, '50--------------')
    # Parse the XML response
    root = ET.fromstring(response.text)

    # Find the TransToken element and get its text value
    trans_token_element = root.find(".//TransToken")
    if trans_token_element is not None:
        trans_token = trans_token_element.text
        data = {
            'trans_token': trans_token
        }
        print("Transaction Token:", trans_token, flush=True)
    else:
        print("TransToken element not found in the XML.")
        data = {
            'error': 'error'
        }

        # print(response.status_code)
        # print(response.text)
    
    return jsonify(data)