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
    

class Profile(models.Model):
    user = models.OneToOneField(CustomeUser, on_delete=models.CASCADE)
    bio = models.CharField(max_length=250, blank=True)
    profile_image = models.ImageField(upload_to='profile_images')


    

SPECIALITIES = (("programming", "programming"),
                ("cybersecurity", "cybersecurty"),
                ("Networking", "networking"))
class Mentor(models.Model):
    user = models.OneToOneField(CustomeUser, on_delete=models.CASCADE)
    field = models.CharField(max_length=200, choices=SPECIALITIES)
    hourly_rate = models.FloatField()
    #add availability here
    # availablities = models.ManyToManyField()

    def __str__(self):
        return self.user.email
    



    
