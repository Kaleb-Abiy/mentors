from django.shortcuts import render
from . models import Speciality, MentorField, Availability, MentorAvailabily, Payment, Appointment
from .serializers import MentorFieldReadSerializer, MentorFieldWriteSerializer, AvailabilityReadSerializer, AvailabilityWriteSerializer, AppointmentWriteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .utils import make_payment, generate_zoom_link
import json
from django.conf import settings
import requests
from .tasks import send_link
# Create your views here.

User = get_user_model()


@api_view(['GET'])
def mentor_list(request):
    fields = None
    hourly_rate = None
    mentors = MentorField.objects.all()
    fields = request.query_params.get('fields', None)
    hourly_rate = request.query_params.get('hourly_rate', None)

    if fields is not None:
        fields_list = fields.split(',')
        mentors = MentorField.objects.filter(fields__name__in=fields_list)
        serializer = MentorFieldReadSerializer(mentors, many=True)
        return Response(serializer.data)
    if hourly_rate is not None:
        mentors = MentorField.objects.filter(hourly_rate__lte=hourly_rate)
        serializer = MentorFieldReadSerializer(mentors, many=True)
        return Response(serializer.data)
    serializer = MentorFieldReadSerializer(mentors, many=True)
    return Response(serializer.data)


@api_view(['POST', 'PUT'])
def mentor_fields_create(request):
    try:
        mentor_field = MentorField.objects.get(user=request.user)
    except MentorField.DoesNotExist:
        mentor_field = None
    if mentor_field and request.method == 'PUT':
        serializer = MentorFieldWriteSerializer(
            data=request.data, instance=mentor_field,  context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    else:
        serializer = MentorFieldWriteSerializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['GET'])
def mentor_detail(request, id):
    mentor = MentorField.objects.get(id=id)
    serializer = MentorFieldReadSerializer(mentor)
    return Response(serializer.data)

@api_view(['POST', 'PUT'])
def set_availability(request):
    
    try:
        mentor_availability = MentorAvailabily.objects.get(mentor=request.user)
    except:
        mentor_availability = None
    
    if mentor_availability and request.method == 'PUT':
        serializer = AvailabilityWriteSerializer(data=request.data, instance=mentor_availability, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    else:
        serializer = AvailabilityWriteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

@api_view(['GET'])
def show(request):
    a = MentorAvailabily.objects.all()
    s = AvailabilityReadSerializer(a, many=True)
    return Response(s.data)

@api_view(['POST'])
def book_appointment(request):
    serializer = AppointmentWriteSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        appointment = serializer.save()
        make_payment(appointment)
        return Response('success')
    return Response(serializer.errors)


@api_view(['POST', 'GET'])
def verify_payment(request):
    data = json.loads(request.body)
    tx = data['trx_ref']
    print(tx)
    if tx:
        headers = {
        'Authorization': f'Bearer {settings.CHAPA_SECRET}',
        'Content-Type': 'application/json'
        }

        res = requests.get(f'https://api.chapa.co/v1/transaction/verify/{tx}', headers=headers)
        if res.status_code == 200:
            payment = Payment.objects.get(tx_ref=tx)
            print(payment.appointment)
            appointment = Appointment.objects.get(payment=payment)
            print(appointment)
            start_date = appointment.appointment_time.date
            start_time = appointment.appointment_time.start_time
            zoom_link = generate_zoom_link(start_date, start_time)
            send_link.delay(request, appointment.booker, appointment.bookee, zoom_link)
            payment.status = 'accepted'
            payment.save()
            appointment.status ='accepted'
            appointment.save()
            

    return Response(request.body)

