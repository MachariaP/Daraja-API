from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword

# Create your views here.
def getAccessToken(request):
    # API credentials for Safaricom's Daraja API
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')

    # URL for M-Pesa OAuth token generation in sandbox environment
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    # Make GET request to M-Pesa API with basic authentication
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

    # Parse the JSON response into a Python dictionary
    mpesa_access_token = json.loads(r.text)

    # Extract the access token from the response dictionary
    validated_mpesa_access_token = mpesa_access_token['access_token']

    # Return the access token as an HTTP response
    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request):
    try:
        access_token = MpesaAccessToken.get_access_token()
    except Exception as e:
        return HttpResponse(f"Error getting access token: {str(e)}", status=500)

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    # Get password and timestamp together
    password, timestamp = LipanaMpesaPpassword.get_password()
    
    payload = {
        "BusinessShortCode": LipanaMpesaPpassword.business_short_code,
        "Password": password,
        "Timestamp": timestamp,  # Now matches password
        "TransactionType": "CustomerPayBillOnline",
        "Amount": "2000",
        "PartyA": "254797204742",
        "PartyB": LipanaMpesaPpassword.business_short_code,
        "PhoneNumber": "254797204742",
        "CallBackURL": "https://yourdomain.com/api/v1/callback",
        "AccountReference": "Diplomat Safes",
        "TransactionDesc": "Test STK Push"
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        return HttpResponse(response.text)
    except requests.RequestException as e:
        return HttpResponse(f"STK Push failed: {str(e)}", status=502)