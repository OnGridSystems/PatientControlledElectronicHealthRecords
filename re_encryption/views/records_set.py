from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from re_encryption.serializers import (
    PublicRecordsSetSerializer,
    RecordsSetUpdateSerializer,
    RecordsSetSerializer
)
from re_encryption.models import RecordsSet
from users.models import Patient
from re_encryption.permissions import (
    OnlyPatientPermission,
    OnlyRecepientPermission,
    RecepientHasReadPermission,
    RecepientHasWritePermission,
    RecepientHasAddPermission
)


class RecordsSetList(generics.ListAPIView):
    serializer_class = PublicRecordsSetSerializer

    def get_queryset(self):
        return RecordsSet.objects.all()
    

class RecordsSetRecepientDetail(generics.RetrieveAPIView):
    permission_classes = (
        IsAuthenticated,
        OnlyRecepientPermission,
        RecepientHasReadPermission
    )
    serializer_class = RecordsSetSerializer
 
    def get_queryset(self):
        return RecordsSet.objects.all()


class RecordsSetRecepientUpdate(generics.UpdateAPIView):
    permission_classes = (
        IsAuthenticated,
        OnlyRecepientPermission,
        RecepientHasWritePermission
    )
    serializer_class = RecordsSetUpdateSerializer
    queryset = RecordsSet.objects.all()


class RecordsSetCreation(generics.CreateAPIView):
    permission_classes = (
        IsAuthenticated,
        OnlyRecepientPermission,
        RecepientHasAddPermission
    )
    serializer_class = RecordsSetSerializer


class RecordsSetOwnList(generics.ListAPIView):
    permission_classes = (IsAuthenticated, OnlyPatientPermission)
    serializer_class = RecordsSetSerializer

    def get_queryset(self):
        return RecordsSet.objects.filter(patient=self.patient)
