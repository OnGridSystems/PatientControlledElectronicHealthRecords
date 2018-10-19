from .models import (
    Patient,
    DataSet
)
from rest_framework import serializers


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Patient
        fields = (
            'first_name', 'last_name',
            'eth_address', 'data_sets',
        )


class PublicDataSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DataSet
        fields = ('name', 'quantity')
