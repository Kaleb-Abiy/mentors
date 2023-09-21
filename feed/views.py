from django.shortcuts import render
from . models import Speciality, MentorField
from .serializers import MentorFieldReadSerializer, MentorFieldWriteSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.


def mentor_list(request):
    pass


@api_view(['POST'])
def mentor_fields_create(request):
    try:
        mentor_field = MentorField.objects.get(user=request.user)
    except MentorField.DoesNotExist:
        mentor_field = None
    if mentor_field:
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
