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



status_choices = (
    ('pending', 'pending'),
    ('accepted', 'accepted'),
    ('rejected', 'rejected'),
)
class Appointment(models.Model):
    booker = models.ForeignKey(User, related_name='booker_appointments', on_delete=models.CASCADE)  # booker
    bookee = models.ForeignKey(User, related_name='bookee_appointments',on_delete=models.CASCADE)  # bookee
    appointment_time = models.ForeignKey(Availability, on_delete=models.CASCADE)
    status = models.CharField(max_length=200, choices=status_choices, default='pending')
    payment = models.OneToOneField('Payment',related_name='appointment', on_delete=models.SET_NULL, null=True, blank=True)
    meeting_link = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return f'{self.booker.email} booked {self.bookee.email} at {self.appointment_time.date} {self.appointment_time.start_time}'
    

class Payment(models.Model):
    amount = models.IntegerField()
    tx_ref = models.CharField(max_length=200)
    payment_by = models.ForeignKey(User, related_name='booker_payments', on_delete=models.CASCADE)
    payment_for = models.ForeignKey(User,related_name='bookee_payments', on_delete=models.CASCADE)
    status = models.CharField(max_length=200, choices=status_choices, default='pending')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.appointment.booker.email} paid {self.amount} for {self.appointment.bookee.email}'


    
    
