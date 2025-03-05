from django.http import HttpResponse, JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
from .models import MpesaPayment

# Load environment variables from .env file
load_dotenv()


def getAccessToken(request):
    # Fetch API credentials from environment variables
    consumer_key = os.getenv('CONSUMER_KEY')
    consumer_secret = os.getenv('CONSUMER_SECRET')

    if not consumer_key or not consumer_secret:
        return HttpResponse("Missing API credentials", status=500)

    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    try:
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        r.raise_for_status()  # Raise exception for HTTP errors
        mpesa_access_token = json.loads(r.text)
        validated_mpesa_access_token = mpesa_access_token['access_token']
        return HttpResponse(validated_mpesa_access_token)
    except requests.RequestException as e:
        return HttpResponse(f"Failed to get access token: {str(e)}", status=500)
    except json.JSONDecodeError as e:
        return HttpResponse(f"Invalid response format: {str(e)}", status=502)


def lipa_na_mpesa_online(request):
    try:
        access_token = MpesaAccessToken.get_access_token()
    except AttributeError as e:
        return HttpResponse(f"Error accessing token: {str(e)}", status=500)

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": "254797204742",  # Replace with your phone number to get STK push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": "254797204742",  # Replace with your phone number to get STK push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Phinehas",
        "TransactionDesc": "Testing stk push"
    }

    try:
        response = requests.post(api_url, json=request, headers=headers)
        response.raise_for_status()
        return HttpResponse('success')
    except requests.RequestException as e:
        return HttpResponse(f"STK Push failed: {str(e)}", status=502)


@csrf_exempt
def register_urls(request):
    try:
        access_token = MpesaAccessToken.get_access_token()
    except AttributeError as e:
        return HttpResponse(f"Error accessing token: {str(e)}", status=500)

    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {
        "ShortCode": LipanaMpesaPpassword.business_short_code,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://f1d9-102-218-124-142.ngrok-free.app/api/v1/c2b/confirmation",
        "ValidationURL": "https://f1d9-102-218-124-142.ngrok-free.app/api/v1/c2b/validation"
    }

    try:
        response = requests.post(api_url, json=options, headers=headers)
        response.raise_for_status()
        return HttpResponse(response.text)
    except requests.RequestException as e:
        return HttpResponse(f"URL registration failed: {str(e)}", status=502)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):
    if request.method != "POST":
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid request method"}, status=405)

    try:
        context = {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }
        return JsonResponse(dict(context))
    except Exception as e:
        return JsonResponse({"ResultCode": 1, "ResultDesc": f"Validation failed: {str(e)}"}, status=500)


@csrf_exempt
def confirmation(request):
    if request.method != "POST":
        return JsonResponse({"ResultCode": 1, "ResultDesc": "Invalid request method"}, status=405)

    try:
        mpesa_body = request.body.decode('utf-8')
        mpesa_payment = json.loads(mpesa_body)

        payment = MpesaPayment(
            first_name=mpesa_payment['FirstName'],
            last_name=mpesa_payment['LastName'],
            middle_name=mpesa_payment['MiddleName'],
            description=mpesa_payment['TransID'],
            phone_number=mpesa_payment['MSISDN'],
            amount=mpesa_payment['TransAmount'],
            reference=mpesa_payment['BillRefNumber'],
            organization_balance=mpesa_payment['OrgAccountBalance'],
            type=mpesa_payment['TransactionType'],
        )
        payment.save()

        context = {
            "ResultCode": 0,
            "ResultDesc": "Accepted"
        }
        return JsonResponse(dict(context))
    except (json.JSONDecodeError, KeyError) as e:
        return JsonResponse({"ResultCode": 1, "ResultDesc": f"Invalid data: {str(e)}"}, status=400)
    except Exception as e:
        return JsonResponse({"ResultCode": 1, "ResultDesc": f"Confirmation failed: {str(e)}"}, status=500)