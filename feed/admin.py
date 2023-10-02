from django.contrib import admin
from .models import Speciality, MentorField, Availability,MentorAvailabily, Payment, Appointment

# Register your models here.
admin.site.register(Speciality)
admin.site.register(MentorField)
admin.site.register(Availability)
admin.site.register(MentorAvailabily)
admin.site.register(Payment)
admin.site.register(Appointment)
