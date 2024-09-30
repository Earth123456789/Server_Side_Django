from rest_framework import serializers
from .models import *
from django.utils import timezone 

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            "id",
            "name",
            "specialization",
            "phone_number",
            "email"
        ]


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = [
            "id",
            "name",
            "phone_number",
            "email",
            "address"
        ]
    
class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)  
    patient = PatientSerializer(read_only=True)  

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'at_time', 'details']
    
    def validate(self, appointment):
        if appointment['date'] < timezone.now() and appointment['at_time'] < timezone.now():
            raise serializers.ValidationError("The appointment date or time must be in the future.")
        return appointment