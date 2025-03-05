import requests
import json
from requests.auth import HTTPBasicAuth
from datetime import datetime
import os
import base64
from dotenv import load_dotenv

load_dotenv()


class MpesaC2bCredential:
    """Store M-Pesa C2B API credentials."""
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"


class MpesaAccessToken:
    """Generate M-Pesa OAuth access token dynamically."""
    
    @classmethod
    def get_access_token(cls):
        """Fetch and return a fresh access token."""
        if not MpesaC2bCredential.consumer_key or not MpesaC2bCredential.consumer_secret:
            raise ValueError("Missing M-Pesa consumer key or secret")
        try:
            r = requests.get(
                MpesaC2bCredential.api_url,
                auth=HTTPBasicAuth(MpesaC2bCredential.consumer_key, MpesaC2bCredential.consumer_secret)
            )
            r.raise_for_status()
            mpesa_access_token = json.loads(r.text)
            return mpesa_access_token['access_token']
        except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
            raise Exception(f"Failed to get access token: {str(e)}")


class LipanaMpesaPpassword:
    """Generate STK Push password for Lipa na M-Pesa Online."""
    business_short_code = "174379"
    passkey = os.getenv('PASSKEY')

    @classmethod
    def get_password(cls):
        """Generate Base64-encoded password with current timestamp."""
        if not cls.passkey:
            raise ValueError("Missing M-Pesa passkey")
        lipa_time = datetime.now().strftime('%Y%m%d%H%M%S')
        data_to_encode = cls.business_short_code + cls.passkey + lipa_time
        online_password = base64.b64encode(data_to_encode.encode())
        return online_password.decode('utf-8'), lipa_time  # Return tuple