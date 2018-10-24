from data_office.models import (
    RecordsSet,
    Patient
)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from data_office.serializers import (
    PublicRecordsSetSerializer,
    ExtendRecordsSetSerializer
)


class RecordsSetList(generics.ListCreateAPIView):
    queryset = RecordsSet.objects.all()
    serializer_class = PublicRecordsSetSerializer
 
    def perform_create(self, serializer):
        patient = Patient.objects.filter(user=self.request.user).first()
        serializer.save(patient=patient)


class RecordsSetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExtendRecordsSetSerializer
 
    def get_queryset(self):
        patient = Patient.objects.filter(user=self.request.user).first()
        return RecordsSet.objects.all().filter(patient=patient)
