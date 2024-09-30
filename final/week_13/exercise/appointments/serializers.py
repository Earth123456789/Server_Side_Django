from rest_framework import serializers
from .models import *
from datetime import datetime 


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

# class AppointmentGetSerializer(serializers.ModelSerializer):
#     doctor = DoctorSerializer(read_only=True)
#     patient = PatientSerializer(read_only=True)
#     class Meta:
#         model = Appointment
#         fields = ['id', 'doctor', 'patient', 'date', 'at_time', 'details']

class AppointmentSerializer(serializers.ModelSerializer):
    doctor_1 = DoctorSerializer(source='doctor', read_only=True)
    patient_1 = PatientSerializer(source='patient', read_only=True)
    doctor = serializers.PrimaryKeyRelatedField(queryset=Doctor.objects.all())
    patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())

    class Meta:
        model = Appointment
        fields = ['id', 'doctor', 'patient', 'date', 'at_time', 'details', 'doctor_1', 'patient_1']
    
    
    def validate(self, data):
        """
        Check that if the language is Python the snippet's title must contains 'django'
        """
        date = data['date']
        time = data['at_time']
        current_date = datetime.now().date()
        current_time = datetime.now().time()

        if date < current_date:
            raise serializers.ValidationError("The appointment date or time must be in the future")
        elif date == current_date and time <= current_time:
            raise serializers.ValidationError("The appointment date or time must be in the future")
        return data
        
