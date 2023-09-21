from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.


class Speciality(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class MentorField(models.Model):
    user = models.OneToOneField(
        User, related_name='fields', on_delete=models.CASCADE)
    fields = models.ManyToManyField(Speciality, related_name='mentors')

    # add availability here(in other table)
    # availablities = models.ManyToManyField()

    def __str__(self):
        return self.user.email
