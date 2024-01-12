from rest_framework import serializers
from . models import MentorField, Speciality, Availability, MentorAvailabily, Appointment
from django.contrib.auth import get_user_model

User = get_user_model()


class SpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Speciality
        fields = '__all__'


class MentorFieldReadSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.email', read_only=True)
    fields = SpecialitySerializer(many=True, read_only=True)

    class Meta:
        model = MentorField
        fields = '__all__'


class MentorFieldWriteSerializer(serializers.ModelSerializer):
    fields = SpecialitySerializer(many=True)

    class Meta:
        model = MentorField
        fields = ['fields', 'hourly_rate']

    def create(self, validated_data):
        fields_data = validated_data.pop('fields', [])
        mentor_field = MentorField.objects.create(
            user=self.context['request'].user, hourly_rate=validated_data['hourly_rate'])
        for field_data in fields_data:
            speciality, _ = Speciality.objects.get_or_create(**field_data)
            mentor_field.fields.add(speciality)
        return mentor_field

    def update(self, instance, validated_data):
        fields_data = validated_data.pop('fields', [])
        if len(fields_data) > 0:
            instance.fields.clear()
            for field_data in fields_data:
                speciality, _ = Speciality.objects.get_or_create(**field_data)
                instance.fields.add(speciality)
        instance.hourly_rate = validated_data.get(
            'hourly_rate', instance.hourly_rate)
        
        return instance
    

class AvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Availability
        fields = ['date', 'start_time', 'end_time']

    


class AvailabilityReadSerializer(serializers.ModelSerializer):
    mentor = serializers.CharField(source = 'mentor.email', read_only=True)
    availability = AvailabilitySerializer(many=True)

    class Meta:
        model= MentorAvailabily
        fields = ['mentor', 'availability']


    
    # def get_times(self, obj):
    #     availablities = obj.availability.all()
    #     times = []
    #     for availability in availablities:
    #         times.append({'start_time': availability.start_time, 'end_time': availability.end_time})
    #     return times

    # def to_representation(self, instance):
    #     res = super().to_representation(instance)
        
    #     grouped_availability = {}
    #     availablities = instance.availability.all()
    #     for availability in availablities:
    #         if str(availability.date) not in grouped_availability:
    #             grouped_availability[str(availability.date)] = []
    #         grouped_availability[str(availability.date)].append(
    #             {'start_time': availability.start_time, 'end_time': availability.end_time})
        
    
            
            
    #     return {
    #             'mentor': instance.mentor.email,
    #             'availability':grouped_availability
    #     }


class AvailabilityWriteSerializer(serializers.ModelSerializer):
    availability = AvailabilitySerializer(many=True)


    class Meta:
        model= MentorAvailabily
        fields = ['availability']

    def create(self, validated_data):
        availability_data = validated_data.pop('availability', [])
        mentor_availability = MentorAvailabily.objects.create(
            mentor=self.context['request'].user)
        for availability in availability_data:
            mentor_availability.availability.add(
                Availability.objects.create(**availability))
        return mentor_availability
    
    def update(self, instance, validated_data):
        availability_data = validated_data.pop('availability', [])
        if len(availability_data) > 0:
            instance.availability.clear()
            for availability in availability_data:
                instance.availability.add(
                    Availability.objects.create(**availability))
        return instance
    

class AppointmentReadSerializer(serializers.ModelSerializer):
    booker = serializers.CharField(source='booker.email', read_only=True)
    bookee = serializers.CharField(source='bookee.email', read_only=True)
    appointment_time = AvailabilitySerializer(many=False, read_only=True)
    class Meta:
        model = Appointment
        exclude = ['payment']


class AppointmentWriteSerializer(serializers.ModelSerializer):
    booker = serializers.HiddenField(default = serializers.CurrentUserDefault())
    appointment_time = serializers.JSONField()

    class Meta:
        model = Appointment
        fields = ['booker', 'bookee', 'appointment_time']

    
    def validate(self, instance):
        appointment_time = instance.get('appointment_time')
        date = appointment_time['date']
        start = appointment_time['start']
        end = appointment_time['end']
        bookee = instance.get('bookee')
        times = Availability.objects.filter(date = date, start_time=start, end_time=end).first()
        if not times:
            raise serializers.ValidationError('No such time available')
        if Appointment.objects.filter(appointment_time=times, booker = self.context['request'].user, bookee=bookee).exists():
            raise serializers.ValidationError('you already booked with this mentor at this time')
        return instance
        

    def create(self, validated_data):
        appointment_time = validated_data.get('appointment_time')
        bookee = validated_data.get('bookee')
        date = appointment_time['date']
        start = appointment_time['start']
        end = appointment_time['end']
        times = Availability.objects.filter(date = date, start_time=start, end_time=end).first()
        print(times)
        appointment = Appointment.objects.create(booker=validated_data['booker'], bookee=bookee, appointment_time=times)
        return appointment



  
          
