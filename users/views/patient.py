from users.models import Patient
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from users.serializers import PatientSignupSerializer


class PatientList(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSignupSerializer


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatientSignupSerializer

    def get_queryset(self):
        return Patient.objects.all().filter(user=self.request.user)


class PatientCreation(generics.CreateAPIView):
    serializer_class = PatientSignupSerializer
