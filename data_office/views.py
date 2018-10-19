from rest_framework import viewsets

from .models import (
    Patient,
    DataSet
)
from .serializers import (
    PatientSerializer,
    PublicDataSetSerializer
)


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DataSetViewSet(viewsets.ModelViewSet):
    queryset = DataSet.objects.all()
    serializer_class = PublicDataSetSerializer
