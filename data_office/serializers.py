from django.contrib.auth.models import User
from rest_framework import serializers

from .models import (
    Patient,
    RecordsSet
)


class UserSerializer(serializers.ModelSerializer):
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


class PatientDetailSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer()

    def create(self, validated_data):
        user = User(
            username=validated_data.get('user').get('username', None)
        )
        user.set_password(validated_data.get('user').get('password', None))
        user.save()

        patient = Patient.objects.create(
            user=user,
            eth_address=validated_data.get('eth_address', None),
            pub_key=validated_data.get('pub_key', None)
        )
        return patient
 
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
        fields = ('eth_address', 'pub_key', 'user')


class PatientListSerializer(serializers.ModelSerializer):
     class Meta:
        model = Patient
        fields = (
            'id', 'username',
            'first_name','last_name'
        )


class PublicRecordsSetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RecordsSet
        fields = ('type', 'id')
