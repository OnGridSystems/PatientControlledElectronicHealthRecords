from django.contrib.auth.models import User
from rest_framework import serializers

from re_encryption.models import (
    RecordsSet,
    Delegation
)
from users.models import Patient


class PublicRecordsSetSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordsSet
        fields = ('type', 'id')


class RecordsSetUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecordsSet
        fields = ('id', 'data', 'capsule')


class RecordsSetSerializer(serializers.Serializer):
    patient_id = serializers.IntegerField()
    type = serializers.CharField()
    data = serializers.CharField()
    capsule = serializers.CharField()

    def create(self, validated_data):
        patient = Patient.objects.get(id=validated_data.get('patient_id'))
        records_set = RecordsSet.objects.create(
            patient=patient,
            type=validated_data.get('type'),
            data=validated_data.get('data'),
            capsule=validated_data.get('capsule')
        )

        return records_set
    
    def save(self):
        pass
