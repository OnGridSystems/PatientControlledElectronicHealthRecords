from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Patient,
    RecordsSet
)


class CreateUserSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = (
            'id', 'username',
            'password', 'first_name',
            'last_name', 'email'
        )

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class UpdateUserSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = (
            'id', 'username',
            'first_name', 'last_name',
        )

        extra_kwargs = {
            'id': {
                'read_only': True
            }
        }


class PatientResetSerializer(serializers.HyperlinkedModelSerializer):
    def update(self, instance, validated_data):
        for field in validated_data:
            if field == 'password':
                instance.user.set_password(validated_data.get(field))
            else:
                instance.__setattr__(field, validated_data.get(field))
        instance.save()

        return instance
 
    class Meta:
        model = Patient
        fields = ('password')
        extra_kwargs = {
            'id': {
                'write_only': True
            }
        }


class PatientSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()
    eth_address = serializers.CharField()
    pub_key = serializers.CharField()

    def create(self, validated_data):
        user = User(
            username=validated_data.get('email', None),
            first_name=validated_data.get('first_name', None),
            last_name=validated_data.get('last_name', None),
        )
        user.set_password(validated_data.get('password', None))
        user.save()

        patient = Patient.objects.create(
            user=user,
            eth_address=validated_data.get('eth_address', None),
            pub_key=validated_data.get('pub_key', None)
        )

        return patient
    
    def save(self):
        pass


class PatientListSerializer(serializers.ModelSerializer):
    user = UpdateUserSerializer()

    class Meta:
        model = Patient
        fields = ('id', 'eth_address', 'user')


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
