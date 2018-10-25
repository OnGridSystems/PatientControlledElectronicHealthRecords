from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from re_encryption.serializers import (
    PublicRecordsSetSerializer,
    RecordsSetSerializer
)
from re_encryption.models import RecordsSet


class RecordsSetList(generics.ListAPIView):
    queryset = RecordsSet.objects.all()
    serializer_class = PublicRecordsSetSerializer


class RecordsSetDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PublicRecordsSetSerializer
 
    def get_queryset(self):
        return RecordsSet.objects.all()


class RecordsSetCreation(generics.CreateAPIView):
    serializer_class = RecordsSetSerializer
