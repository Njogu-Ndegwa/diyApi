from os.path import join
from pathlib import Path
from flask import Flask, Blueprint
from dotenv import load_dotenv
import requests

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
load_dotenv(join(BASE_PATH, '.env'))

card_payment_api = Blueprint('card_payment_api', __name__)

@card_payment_api.route('/card-payment', methods=['GET'])

def card_payment():
    url = "https://secure.3gdirectpay.com/API/v6/"
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml"
    }

    xml_data = '''
<?xml version="1.0" encoding="utf-8"?>
<API3G>
  <CompanyToken>8D3DA73D-9D7F-4E09-96D4-3D44E7A83EA3</CompanyToken>
  <Request>chargeTokenCreditCard</Request>
  <TransactionToken>9E5EC8D4-7BD0-4924-A006-98D04816AEEE</TransactionToken>
  <CreditCardNumber>5436886269848307</CreditCardNumber>
  <CreditCardExpiry>1224</CreditCardExpiry>
  <CreditCardCVV>123</CreditCardCVV>
  <CardHolderName>John Doe</CardHolderName>
  <ChargeType></ChargeType>
  <ThreeD>
    <Enrolled>Y</Enrolled>
    <Paresstatus>Y</Paresstatus>
    <Eci>05</Eci>
    <Xid>DYYVcrwnujRMnHDy1wlP1Ggz8w0=</Xid>
    <Cavv>mHyn+7YFi1EUAREAAAAvNUe6Hv8=</Cavv>
    <Signature>_</Signature>
    <Veres>AUTHENTICATION_SUCCESSFUL</Veres>
    <Pares>eAHNV1mzokgW/isVPY9GFSCL0EEZkeyg7</Pares>
  </ThreeD>
</API3G>
    '''

    response = requests.post(url, headers=headers, data=xml_data)

    print(response.status_code)
    print(response.text)

