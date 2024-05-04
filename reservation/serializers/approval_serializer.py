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

    def validate_status(self, value):
        if value not in (-1, 0, 1):
            raise serializers.ValidationError("Invalid status for approval.")
        return value

    class Meta:
        model = Approval
        fields = ['id', 'event', 'requesitioner', 'status',
                  'immediate_head_approver', 'person_in_charge_approver']
