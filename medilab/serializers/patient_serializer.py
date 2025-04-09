from rest_framework import serializers
from django.contrib.auth import get_user_model
import base64
from medilab.models import PatientProfile, PatientProfileApplication

User = get_user_model()


class PatientProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)

    class Meta:
        model = PatientProfile
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "address",
            "village",
            "medical_history",
            "approved_by",
            "approval_date",
            "created_at",
        ]
        read_only_fields = ["approved_by", "approval_date"]


class Base64ImageField(serializers.Field):
    def to_representation(self, value):
        if not value:
            return None
        return {"filename": value.id_proof_filename, "data": value.id_proof_base64}

    def to_internal_value(self, data):
        if isinstance(data, dict):
            return {
                "id_proof_base64": data.get("data"),
                "id_proof_filename": data.get("filename"),
            }
        return {
            "id_proof_base64": data,
            "id_proof_filename": "id_proof.jpg",  # Default filename
        }


class PatientProfileApplicationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    first_name = serializers.CharField(source="user.first_name", read_only=True)
    last_name = serializers.CharField(source="user.last_name", read_only=True)
    id_proof = Base64ImageField(source="*")

    class Meta:
        model = PatientProfileApplication
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "address",
            "village",
            "id_proof",
            "medical_history",
            "status",
            "reviewed_by",
            "review_date",
            "created_at",
        ]
        read_only_fields = ["status", "reviewed_by", "review_date", "user"]


class PatientProfileApplicationCreateSerializer(serializers.ModelSerializer):
    id_proof = Base64ImageField(source="*", required=True)

    class Meta:
        model = PatientProfileApplication
        fields = ["date_of_birth", "address", "village", "id_proof", "medical_history"]


class ApplicationReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientProfileApplication
        fields = ["status"]

    def update(self, instance, validated_data):
        request = self.context.get("request")
        if not request or not request.user.is_staff:
            raise serializers.ValidationError("Only staff can review applications")

        new_status = validated_data.get("status")

        if new_status == "approved":
            instance.approve(request.user)
        elif new_status == "rejected":
            instance.reject(request.user)
        else:
            raise serializers.ValidationError("Invalid status")

        return instance


# NEW SERIALIZER FOR UPDATE REQUESTS:
class PatientProfileUpdateSerializer(serializers.ModelSerializer):
    """Special serializer that creates update applications instead of direct updates"""

    class Meta:
        model = PatientProfile
        fields = ["date_of_birth", "address", "village", "medical_history"]

    def update(self, instance, validated_data):
        # OVERRIDDEN: Creates update application instead of updating directly
        instance.create_update_application(validated_data)
        return instance  # Still return instance (though it wasn't modified)
