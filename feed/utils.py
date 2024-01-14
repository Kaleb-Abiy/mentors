import requests
import json
from . models import MentorField
import random
import string
from django.conf import settings
from .models import Payment
from django.shortcuts import redirect

def genrate_tx():
    S = 10  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
    print("The randomly generated string is : " + str(ran)) # print the random data
    return ran  


def make_payment(request, appointment):
    host = request.META['HTTP_HOST']
    mentor = appointment.bookee
    rate = MentorField.objects.get(user = mentor).hourly_rate
    tx = genrate_tx()
    payload = json.dumps({
        "amount": rate,
        "currency": "ETB",
        "email": mentor.email,
        "first_name": "Bilen",
        "last_name": "Gizachew",
        "phone_number": "0912345678",
        "tx_ref": tx,
        "callback_url": f"https://{host}/mentors/verify/",
        "customization[title]": "Payment for my favourite merchant",
        "customization[description]": "I love online payments"
    })

    headers = {
    'Authorization': f'Bearer {settings.CHAPA_SECRET}',
    'Content-Type': 'application/json'
    }
    payments = requests.post(url='https://api.chapa.co/v1/transaction/initialize', data=payload,headers=headers)
    print(payments.json())
    payment = Payment.objects.create(amount=rate, tx_ref=tx, payment_by=appointment.booker, payment_for=appointment.bookee)
    appointment.payment = payment
    appointment.save()



def generate_zoom_link(start_date, start_time):
    auth_token_url = "https://zoom.us/oauth/token"
    api_base_url = "https://api.zoom.us/v2"
    data = {
        "grant_type": "account_credentials",
        "account_id": settings.ZOOM_ACCOUNT_ID,
        "client_secret": settings.ZOOM_CLIENT_SECRET,
    }

    response = requests.post(auth_token_url,
                             auth=(settings.ZOOM_CLIENT_ID,
                                   settings.ZOOM_CLIENT_SECRET),
                             data=data)
    if response.status_code!=200:
        print("Unable to get access token")
    response_data = response.json()
    access_token = response_data["access_token"]
    print(access_token)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "topic":'mentorship',
        "duration": '45',
        'start_time': f'{start_date}T10: {start_time}',
        "type": 2
    }

    resp = requests.post(f"{api_base_url}/users/me/meetings",
                         headers=headers,
                         json=payload)
    if resp.status_code!=201:
            print("Unable to generate meeting link")
    response_data = resp.json()
    
    content = {
                "meeting_url": response_data["join_url"], 
                "password": response_data["password"],
                "meetingTime": response_data["start_time"],
                "purpose": response_data["topic"],
                "duration": response_data["duration"],
                "message": "Success",
                "status":1
    }
    print(content)
    return content


# def verify_payment(tx):
#     headers = {
#     'Authorization': f'Bearer {settings.CHAPA_SECRET}',
#     'Content-Type': 'application/json'
#     }

#     res = requests.get(f'https://api.chapa.co/v1/transaction/verify/{tx}')
     
#     print(res)
        