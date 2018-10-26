from rest_framework import serializers

from re_encryption.models import (
    RecordsSet,
    Delegation
)
from users.models import Recepient


class RecordsDelegationSerializer(serializers.Serializer):
    records_set_id = serializers.IntegerField()
    type = serializers.CharField()
    recepient_id = serializers.IntegerField()

    def create(self, validated_data):
        records_set = RecordsSet.objects.get(id=validated_data.get('records_set_id'))
        recepient = Recepient.objects.get(id=validated_data.get('recepient_id'))
        delegation = Delegation.objects.create(
            records_set=records_set,
            type=validated_data.get('type'),
            recepient=recepient
        )

        return delegation
