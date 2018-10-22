from rest_framework import viewsets

from .models import (
    Patient,
    RecordsSet
)
from .serializers import (
    PatientSerializer,
    PublicRecordsSetSerializer
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class RecordsSetViewSet(viewsets.ModelViewSet):
    queryset = RecordsSet.objects.all()
    serializer_class = PublicRecordsSetSerializer
