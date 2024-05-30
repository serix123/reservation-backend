from rest_framework import serializers
from reservation.models import Employee, Department, Facility
from reservation.serializers.event_serializer import EventSerializer


class FacilitySerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)
    # Make the ID field read-only
    id = serializers.IntegerField(read_only=True)
    person_in_charge = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,  # Not required for updates
        allow_null=True,  # Allows the person_in_charge to be null
    )

    class Meta:
        model = Facility
        fields = [
            "id",
            "name",
            "department",
            "facility_description",
            "person_in_charge",
            "events",
            "image",
        ]

    def validate_image(self, value):
        if not value.name.endswith((".jpg", ".jpeg", ".png")):
            raise serializers.ValidationError(
                "Unsupported file format. Only JPG, JPEG, PNG, and PDF are allowed."
            )
        return value

    def validate_id(self, value):
        """
        Check that the id is not being modified.
        """
        if self.instance and self.instance.id != value:
            raise serializers.ValidationError("ID cannot be modified.")
        return value
    
    def validate_event_file(self, value):
        if value is not None and not value.name.endswith(
            (".jpg", ".jpeg", ".png", ".pdf")
        ):
            raise serializers.ValidationError(
                "Unsupported file format. Only JPG, JPEG, PNG, and PDF are allowed."
            )
        return value


    def create(self, validated_data):
        if "department" not in validated_data:
            # Fetch the first department to use as a default
            default_department = Department.objects.first()
            if not default_department:
                raise serializers.ValidationError("No default department available.")
            validated_data["department"] = default_department
        if "person_in_charge" not in validated_data:
            # Fetch the first department to use as a default
            default_person_in_charge = Employee.objects.first()
            if not default_person_in_charge:
                raise serializers.ValidationError(
                    "No default person_in_charge available."
                )
            validated_data["person_in_charge"] = default_person_in_charge
        return super().create(validated_data)
