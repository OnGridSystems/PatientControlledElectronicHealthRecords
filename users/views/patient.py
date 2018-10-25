from users.models import Patient
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated

from users.serializers import PatientSignupSerializer
from users.permissions import AnonymousPermission


class PatientList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Patient.objects.all()
    serializer_class = PatientSignupSerializer


class PatientDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PatientSignupSerializer
    queryset = Patient.objects.all()


class PatientCreation(generics.CreateAPIView):
    permission_classes = (AnonymousPermission,)
    serializer_class = PatientSignupSerializer
    queryset = Patient.objects.all()
