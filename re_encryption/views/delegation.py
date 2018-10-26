from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from re_encryption.serializers import RecordsDelegationSerializer
from re_encryption.permissions import OnlyPatientPermission


class RecordsDelegationCreation(generics.CreateAPIView):
    permission_classes = (
        IsAuthenticated,
        OnlyPatientPermission
    )
    serializer_class = RecordsDelegationSerializer
