from .models import (
    Patient,
    RecordsSet
)
from rest_framework import serializers


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient
        fields = (
            'first_name', 'last_name',
            'eth_address', 'data_sets',
        )


class PublicRecordsSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecordsSet
        fields = ('type', 'id')
