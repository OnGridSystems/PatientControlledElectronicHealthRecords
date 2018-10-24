from rest_framework import serializers

from data_office.models import Patient


USER_FIELDS = ['first_name', 'last_name', 'email', 'password']

class PatientSignupSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
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

    def update(self, instance, validated_data):
        for field in validated_data:
            if field == 'password':
                instance.user.set_password(validated_data.get(field))
            elif field in USER_FIELDS:
                instance.user.__setattr__(field, validated_data.get(field))
            else:
                instance.__setattr__(field, validated_data.get(field))
        instance.save()

        return instance
    
    def save(self):
        pass
