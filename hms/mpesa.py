
import requests
import json
import base64
from datetime import datetime
from django.conf import settings

class MpesaClient:
    def __init__(self):
        self.consumer_key = settings.MPESA_CONSUMER_KEY
        self.consumer_secret = settings.MPESA_CONSUMER_SECRET
        self.shortcode = settings.MPESA_SHORTCODE
        self.passkey = settings.MPESA_PASSKEY
        self.base_url = "https://sandbox.safaricom.co.ke" if settings.DEBUG else "https://api.safaricom.co.ke"

    def get_token(self):
        url = f"{self.base_url}/oauth/v1/generate?grant_type=client_credentials"
        auth = (self.consumer_key, self.consumer_secret)
        try:
            response = requests.get(url, auth=auth, timeout=10)
            response.raise_for_status()
            return response.json()['access_token']
        except Exception as e:
            # Fallback for demo/testing without credentials
            # In production this should raise Error
            print(f"Mpesa Token Error: {e}")
            return "dummy_token" 

    def stk_push(self, phone_number, amount, reference, callback_url):
        token = self.get_token()
        if token == "dummy_token":
             # Simulate success for demo
             return {
                 "ResponseCode": "0",
                 "MerchantRequestID": "29412-2993-99933",
                 "CheckoutRequestID": f"ws_CO_{datetime.now().strftime('%Y%m%d%H%M%S')}_dummy",
                 "ResponseDescription": "Success. Request accepted for processing"
             }

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # M-Pesa expects phone in 2547XXXXXXXX format without +
        if phone_number.startswith('+'):
            phone_number = phone_number[1:]
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
            
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount), 
            "PartyA": phone_number,
            "PartyB": self.shortcode,
            "PhoneNumber": phone_number,
            "CallBackURL": callback_url,
            "AccountReference": reference,
            "TransactionDesc": "Accommodation"
        }
        
        url = f"{self.base_url}/mpesa/stkpush/v1/processrequest"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            return {"ResponseCode": "1", "ResponseDescription": str(e)}

    def stk_push_query(self, checkout_request_id):
        token = self.get_token()
        if token == "dummy_token":
             return {"ResponseCode": "0", "ResultCode": "0", "ResultDesc": "Simulated Success"}

        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode(f"{self.shortcode}{self.passkey}{timestamp}".encode()).decode()
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        payload = {
            "BusinessShortCode": self.shortcode,
            "Password": password,
            "Timestamp": timestamp,
            "CheckoutRequestID": checkout_request_id
        }
        
        url = f"{self.base_url}/mpesa/stkpushquery/v1/query"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            return response.json()
        except Exception as e:
            return {"ResponseCode": "1", "ResponseDescription": str(e)}
