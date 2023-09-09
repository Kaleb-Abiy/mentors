from rest_framework import serializers
from .models import CustomeUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length=250, write_only=True)
    password2 = serializers.CharField(max_length=250, write_only=True)
    role = serializers.CharField(max_length=200)

    class Meta:
        model = CustomeUser
        fields = ['email', 'password1', 'password2', 'role']

    def validate(self, attrs):
        if (attrs['password1'] != attrs['password2']):
            raise ValueError('password dont match')
        return super().validate(attrs)

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password1']
        role = validated_data['role']
        user = CustomeUser(email=email)
        user.set_password(password)
        if role == 'mentor':
            user.is_mentor = True
        elif role == 'user':
            user.is_user = True
        user.is_active = False
        user.save()
        return user
