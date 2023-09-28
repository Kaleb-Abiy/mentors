from rest_framework import serializers
from . models import MentorField, Speciality, Availability, MentorAvailabily


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

    def to_representation(self, instance):
        res = super().to_representation(instance)
        
        grouped_availability = {}
        availablities = instance.availability.all()
        for availability in availablities:
            if str(availability.date) not in grouped_availability:
                grouped_availability[str(availability.date)] = []
            grouped_availability[str(availability.date)].append(
                {'start_time': availability.start_time, 'end_time': availability.end_time})
        
    
            
            
        return {
                'mentor': instance.mentor.email,
                'availability':grouped_availability
        }
  
          
