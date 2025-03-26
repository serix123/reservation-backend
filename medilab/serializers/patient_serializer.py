from rest_framework import serializers
from medilab.models import Patient
from django.contrib.auth.models import User


class PatientSerializer(serializers.ModelSerializer):
    """
    Serializer for the Patient model to handle data conversion 
    between complex data types and Python/JSON representations.
    """
    # Optional: Add custom fields or validation
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Patient
        fields = [
            'id',
            'user',
            'first_name',
            'last_name',
            'full_name',
            'birthdate',
            'gender',
            'address',
            'age',
            'email',
            'phone_number',
        ]
        extra_kwargs = {
            'user': {'required': False}  # Make user optional in serialization
        }

    def get_full_name(self, obj):
        """
        Custom method to generate full name dynamically.
        """
        return f"{obj.first_name} {obj.last_name}"

    def get_age(self, obj):
        """
        Calculate patient's age based on birthdate.
        """
        from datetime import date
        today = date.today()
        return today.year - obj.birthdate.year - (
            (today.month, today.day) < (obj.birthdate.month, obj.birthdate.day)
        )

    def create(self, validated_data):
        """
        Custom create method to handle potential user context.
        """
        # If no user provided, try to get from request context
        user = validated_data.pop('user', None)
        if not user and hasattr(self, '_user'):
            user = self._user

        patient = Patient.objects.create(user=user, **validated_data)
        return patient
