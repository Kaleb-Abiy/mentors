from django.shortcuts import render
from . models import Speciality, MentorField, Availability, MentorAvailabily
from .serializers import MentorFieldReadSerializer, MentorFieldWriteSerializer, AvailabilityReadSerializer, AvailabilityWriteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
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
