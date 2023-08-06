from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import CustomeUserManager


# Create your models here.


class CustomeUser(AbstractUser):
    username = None
    is_user = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    

    objects = CustomeUserManager()


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    ordering = ('email',)
    

    def __str__(self):
        return self.email

    
