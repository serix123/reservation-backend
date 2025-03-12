from rest_framework import serializers
from residence.models import Residence
from django.contrib.auth import get_user_model

User = get_user_model()


class ResidenceSerializer(serializers.ModelSerializer):
    user_email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Residence
        fields = [
            'id',
            'user_email',
            'first_name',
            'last_name',
            'role',
            'contact_number',
            'address',
            'registration_date'
        ]
        read_only_fields = ('registration_date',)


class CreateResidenceSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    class Meta:
        model = Residence
        fields = [
            'email',
            'first_name',
            'last_name',
            'role',
            'contact_number',
            'address'
        ]

    def create(self, validated_data):
        email = validated_data.pop('email')
        try:
            # Case-insensitive email lookup
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"email": "User with this email does not exist"}
            )

        if hasattr(user, 'residence'):
            raise serializers.ValidationError(
                {"email": "This user already has a residence record"}
            )

        # Use user's names if not provided
        first_name = validated_data.pop('first_name', user.first_name)
        last_name = validated_data.pop('last_name', user.last_name)

        return Residence.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            **validated_data
        )
