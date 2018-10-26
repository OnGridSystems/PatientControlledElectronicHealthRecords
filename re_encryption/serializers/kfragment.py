from rest_framework import serializers

from re_encryption.models import (
    KeyFragment,
    Delegation
)


class KfragmentSerializer(serializers.Serializer):
    delegation_id = serializers.IntegerField()
    bytes = serializers.CharField()

    def create(self, validated_data):
        delegation = Delegation.objects.get(id=validated_data.get('delegation_id'))
        kfrag = KeyFragment.objects.create(
            delegation=delegation,
            bytes=validated_data.get('bytes')
        )

        return kfrag
