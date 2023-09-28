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
    hourly_rate = models.IntegerField(blank=True)

    # add availability here(in other table)
    # availablities = models.ManyToManyField()

    def __str__(self):
        return self.user.email


class Availability(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    


class MentorAvailabily(models.Model):
    mentor = models.OneToOneField(User, on_delete=models.CASCADE)
    availability = models.ManyToManyField(Availability)

    def __str__(self):
        return f'{self.mentor.email} availabilities'

    
    
