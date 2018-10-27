from rest_framework import serializers

from re_encryption.models import (
    RecordsSet,
    ReEncryption
)


class ReEncryptionSerializer(serializers.Serializer):
    records_set_id = serializers.IntegerField()
    verifying_key = serializers.CharField()
    recepient_id = serializers.IntegerField()

    def create(self, validated_data):
        records_set = RecordsSet.objects.get(id=validated_data.get('records_set_id'))
        re_encryption = ReEncryption.objects.create(
            records_set=records_set,
            verifying_key=validated_data.get('verifying_key'),
            recepient_id=validated_data.get('recepient_id')
        )

        return re_encryption
