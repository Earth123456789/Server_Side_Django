from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Doctor, Patient, Appointment  
from .serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer
from django.http import Http404


# Create your views here.
class DoctorList(APIView):
    def get(self, request, format=None):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

class PatientList(APIView):
    def get(self, request, format=None):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

class AppointmentList(APIView):
    def get(self, request, format=None):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
class AppointmentDetailList(APIView):

    def get_object(self, pk):
        try:
            return Appointment.objects.get(pk=pk)
        except Appointment.DoesNotExist:
            raise Http404
    
    def get(self, request, id, format=None):
        appointments = self.get_object(id)
        serializer = AppointmentSerializer(appointments)
        return Response(serializer.data)
    
    def put(self, request, id, format=None):
        appointments = self.get_object(id)
        serializer = AppointmentSerializer(appointments,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        appointments = self.get_object(id)
        appointments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)