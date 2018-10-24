from django.contrib.auth.models import User
from rest_framework import serializers

from users.models import (
    Patient,
    RecordsSet
)


class PublicRecordsSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecordsSet
        fields = ('type', 'id')


class CreateRecordsSetSerializer(serializers.HyperlinkedModelSerializer):
    patient_id = serializers.IntegerField()

    def create(self, validated_data):
        patient = Patient.objects.get(id=validated_data.get('patient_id'))
        records_set = RecordsSet.objects.create(
            patient=patient,
            type=validated_data.get('type'),
            data=validated_data.get('data'),
            caplsule=validated_data.get('capsule')
        )

        return records_set

    class Meta:
        model = RecordsSet


class ExtendRecordsSetSerializer(serializers.HyperlinkedModelSerializer):
    pass
