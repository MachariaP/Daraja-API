from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
import os

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
