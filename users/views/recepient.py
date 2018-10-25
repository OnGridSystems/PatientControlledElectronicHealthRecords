from users.models import Recepient
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated

from users.serializers import RecepientSerializer
from users.permissions import AnonymousPermission


class RecepientList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Recepient.objects.all()
    serializer_class = RecepientSerializer


class RecepientDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = RecepientSerializer


class RecepientCreation(generics.CreateAPIView):
    permission_classes = (AnonymousPermission,)
    serializer_class = RecepientSerializer
