from rest_framework import serializers
from medilab.models import MedicalRecord
from medilab.serializers import PatientProfileSerializer


class MedicalRecordSerializer(serializers.ModelSerializer):
    """
    Serializer for MedicalRecord model to handle data conversion
    and provide additional context.
    """
    # Optional: Include patient details
    patient_details = PatientProfileSerializer(source="patient", read_only=True)

    # Optional: Custom doctor name retrieval
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = MedicalRecord
        fields = [
            'id',
            'patient',
            'patient_details',
            'visit_date',
            'diagnosis_category',
            'diagnosis_details',
            'treatment',
            'attending_doctor',
            'doctor_name',
            'notes',
            'follow_up_date'
        ]
        extra_kwargs = {
            'patient': {'required': True},
            'attending_doctor': {'required': False}
        }

    def get_doctor_name(self, obj):
        """
        Retrieve the full name of the attending doctor.
        """
        if obj.attending_doctor:
            return f"{obj.attending_doctor.first_name} {obj.attending_doctor.last_name}"
        return "Unknown"

    def create(self, validated_data):
        """
        Custom create method to handle context and default values.
        """
        # If no doctor provided, use the current user (if authenticated)
        if 'attending_doctor' not in validated_data:
            user = self.context.get('request').user
            validated_data['attending_doctor'] = user

        return super().create(validated_data)
