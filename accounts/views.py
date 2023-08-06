from django.shortcuts import render
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view
from . utils import get_tokens_for_user

# Create your views here.
@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response(tokens)
    else:
        return Response(serializer.errors)
    
