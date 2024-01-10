from django.shortcuts import render, redirect
from .serializers import UserRegisterSerializer, ProfileSerializer
from rest_framework.response import Response
from django.http.response import HttpResponse
from django.http import HttpResponse
from rest_framework.decorators import api_view
from . utils import get_tokens_for_user, send_email_verfication, check_confirmation_token
from django.contrib.auth import get_user_model
from .models import CustomeUser, Profile
from drf_spectacular.utils import extend_schema, OpenApiTypes as Type
from rest_framework import status

User = get_user_model()

# Create your views here.


@extend_schema(
        description='Takes email, user role("user", "mentor") and password to register users it generates access token and referesh token after succesful registration',
        request=UserRegisterSerializer,
        responses={
            status.HTTP_201_CREATED: {
                'type': 'object',
                'properties': {
                        'access': {'type': 'string'},
                        'refresh': {'type': 'string'}
                }
            },
            status.HTTP_400_BAD_REQUEST: {
                'type': 'object',
                'properties': {
                        'error': {'type': 'string'}
                }
            }
        }
)
@api_view(['POST'])
def register_user(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        send_email_verfication(request, user)
        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_201_CREATED)
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



@extend_schema(
        description='Updates user profile',
        request=ProfileSerializer,
        responses= {
            status.HTTP_200_OK: {
                'type': 'string',
                'properties': {
                    'message': 'created'
                }
            },
            status.HTTP_400_BAD_REQUEST: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
)
@api_view(['PUT'])
def update_profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response('created', status=status.HTTP_200_OK)
    except Exception as e:
        Response('no profile with this user')
