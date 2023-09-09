from django.shortcuts import render, redirect
from .serializers import UserRegisterSerializer
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.http import HttpResponse
from rest_framework.decorators import api_view
from . utils import get_tokens_for_user, send_email_verfication, check_confirmation_token
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your views here.


@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_email_verfication(request, user)
        tokens = get_tokens_for_user(user)
        return Response(tokens)
    else:
        return Response(serializer.errors)


def verify_user(request):
    user_id = request.GET['user_id']
    token = request.GET['token']

    print(user_id)
    print(token)

    try:
        user = User.objects.get(id=user_id)
        if user.is_active:
            return HttpResponse('already verfied')
        valid_token = check_confirmation_token(user, token)
        if valid_token:
            user.is_active = True
            user.save()
            return HttpResponse('succeed')
        else:
            return HttpResponse('fail')
    except Exception as e:
        return HttpResponse(e)
