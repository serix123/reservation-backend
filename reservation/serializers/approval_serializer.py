from rest_framework import serializers
from reservation.models import Approval, Employee


class ApprovalSerializer(serializers.ModelSerializer):
    requesitioner = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,  # Not required for updates
        allow_null=True,  # Allows the person_in_charge to be null
    )
    immediate_head_approver = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,  # Not required for updates
        allow_null=True,  # Allows the person_in_charge to be null
    )
    person_in_charge_approver = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,  # Not required for updates
        allow_null=True,  # Allows the person_in_charge to be null
    )
    # immediate_head_approver = serializers.ReadOnlyField()
    # person_in_charge_approver = serializers.ReadOnlyField()
    # admin_approver = serializers.PrimaryKeyRelatedField(read_only=True)

    def validate_status(self, value):
        if value not in (-1, 0, 1):
            raise serializers.ValidationError("Invalid status for approval.")
        return value

    event_details = serializers.SerializerMethodField()

    def get_event_details(self, obj):
        if obj.event:
            return {
                "id": obj.event.id,
                "event_name": obj.event.event_name,
                "event_description": obj.event.event_description,
                # "requesitioner": obj.event.requesitioner,
                "contact_number": obj.event.contact_number,
                # "reserved_facility": obj.event.reserved_facility,
                "participants_quantity": obj.event.participants_quantity,
                "department": obj.event.department,
                "start_time": obj.event.start_time,
                "end_time": obj.event.end_time,
                # "equipments": obj.event.equipments,
                "status": obj.event.status,
                "additional_needs": obj.event.additional_needs,
                "slip_number": obj.event.slip_number,
            }
        return None

    # def to_representation(self, instance):
    #     # Call the parent class's to_representation method
    #     data = super().to_representation(instance)

    #     # Check if the request method is GET
    #     if self.context["request"].method == "GET":
    #         # Include admin_approver in the response
    #         data["admin_approver"] = (
    #             instance.admin_approver.id if instance.admin_approver else None
    #         )

    #     return data

    class Meta:
        model = Approval
        fields = [
            "id",
            "slip_number",
            "event",
            "event_details",
            "requesitioner",
            "status",
            "status_update_date",
            "immediate_head_approver",
            "person_in_charge_approver",
            # "admin_approver",
            "immediate_head_status",
            "person_in_charge_status",
            "admin_status",
            "immediate_head_update_date",
            "person_in_charge_update_date",
            "admin_update_date",
        ]
        extra_kwargs = {
            # "admin_approver": {"required": False, "allow_null": True},
        }
