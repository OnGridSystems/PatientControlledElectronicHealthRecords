from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from re_encryption.serializers import KfragmentSerializer
from re_encryption.permissions import OnlyPatientPermission
from re_encryption.models import KeyFragment


class KfragmentListCreate(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = KeyFragment.objects.all()
    serializer_class = KfragmentSerializer
