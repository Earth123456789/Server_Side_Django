from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from .models import Doctor, Patient, Appointment  
from .serializers import DoctorSerializer, PatientSerializer, AppointmentSerializer
from django.http import Http404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from .permission import AppointmentPermission
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import permissions

# Create your views here.

class MyTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"


class DoctorList(APIView):
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        print(request.user)
        print(request.auth)

        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

class PatientList(APIView):
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):

        print(request.user)
        print(request.auth)

        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

class AppointmentList(APIView):
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, AppointmentPermission]

    def get(self, request, format=None):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)
    

    def post(self, request, format=None):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
class AppointmentDetailList(APIView):
    authentication_classes = [MyTokenAuthentication]
    permission_classes = [IsAuthenticated, AppointmentPermission]

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
        self.check_object_permissions(request, appointments)
        serializer = AppointmentSerializer(appointments,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, id, format=None):
        appointments = self.get_object(id)
        self.check_object_permissions(request, appointments)
        appointments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



