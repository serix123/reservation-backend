# serializers.py
from rest_framework import serializers
from medilab.models import Patient
from django.contrib.auth import get_user_model

User = get_user_model()


class PatientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "dob",
            "gender",
            "contact_number",
            "address",
            "verification_status",
            "id_document",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["verification_status", "created_at", "updated_at"]

    def to_representation(self, instance):
        """
        Custom representation to control which fields are shown based on user permissions.
        - Staff users see all fields
        - Non-staff users (owners) see all fields except verification_status
        - Other users see basic fields without sensitive data
        """
        representation = super().to_representation(instance)
        request = self.context.get("request")

        if request and (request.user.is_staff or instance.user == request.user):
            # Staff or owner can see all fields except verification_status for non-staff
            # if not request.user.is_staff:
            #     representation.pop("verification_status", None)
            return representation

        # For other users (shouldn't happen due to permissions, but just in case)
        representation.pop("id_document", None)
        representation.pop("verification_status", None)
        return representation


class PatientVerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Patient
        fields = [
            "id",
            "first_name",
            "last_name",
            "dob",
            "gender",
            "contact_number",
            "address",
            "id_document",
            "verification_status",
            "email",
            "created_at",
        ]
        read_only_fields = fields  # All fields are read-only for staff viewing
