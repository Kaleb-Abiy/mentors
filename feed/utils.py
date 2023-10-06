import requests
import json
from . models import MentorField
import random
import string
from django.conf import settings


def genrate_tx():
    S = 10  # number of characters in the string.  
    # call random.choices() string module to find the string in Uppercase + numeric data.  
    ran = ''.join(random.choices(string.ascii_uppercase + string.digits, k = S))    
    print("The randomly generated string is : " + str(ran)) # print the random data
    return ran  


def make_payment(appointment):
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
        "callback_url": "https://127.0.0.1:8000",
        "return_url": "https://127.0.0.1:8000",
        "customization[title]": "Payment for my favourite merchant",
        "customization[description]": "I love online payments"
    })

    headers = {
    'Authorization': f'Bearer {settings.CHAPA_SECRET}',
    'Content-Type': 'application/json'
    }
    payment = requests.post(url='https://api.chapa.co/v1/transaction/initialize', data=payload,headers=headers)
    print(payment.json())