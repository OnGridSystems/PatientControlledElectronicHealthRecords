from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from re_encryption.serializers import KfragmentSerializer
from re_encryption.permissions import OnlyPatientPermission


class KfragmentListCreate(generics.ListCreateAPIView):
    permission_classes = (
        IsAuthenticated,
        OnlyPatientPermission
    )
    serializer_class = KfragmentSerializer
