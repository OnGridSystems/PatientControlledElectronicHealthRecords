from rest_framework import serializers

from re_encryption.models import KeyFragment


class KfragmentSerializer(serializers.Serializer):
    delegation_id = serializers.IntegerField()
    bytes = serializers.CharField()
