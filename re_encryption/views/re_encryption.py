from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from re_encryption.serializers import (
    ReEncryptionSerializer
)
from re_encryption.models import ReEncryption


class ReEncryptionCreation(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReEncryptionSerializer

    def get_queryset(self):
        return ReEncryption.objects.filter(recepient_id=self.request.user.id)


class ReEncryptionDetail(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ReEncryptionSerializer
 
    def get_queryset(self):
        return ReEncryption.objects.filter(recepient_id=self.request.user.id)
