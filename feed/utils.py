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


def make_payment(appointment):
    from feed.views import verify_payment
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
        "callback_url": "https://115f-196-189-240-248.ngrok-free.app//feed/verify/",
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
    


# def verify_payment(tx):
#     headers = {
#     'Authorization': f'Bearer {settings.CHAPA_SECRET}',
#     'Content-Type': 'application/json'
#     }

#     res = requests.get(f'https://api.chapa.co/v1/transaction/verify/{tx}')
     
#     print(res)
        