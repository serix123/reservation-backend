from rest_framework import serializers
from reservation.models import Approval, Employee


class ApprovalSerializer(serializers.ModelSerializer):
    applicant = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,  # Not required for updates
        allow_null=True,  # Allows the person_in_charge to be null
    )
    l1_approver = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,  # Not required for updates
        allow_null=True,  # Allows the person_in_charge to be null
    )
    l2_approver = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,  # Not required for updates
        allow_null=True,  # Allows the person_in_charge to be null
    )

    class Meta:
        model = Approval
        fields = ['id', 'event', 'applicant', 'status',
                  'l1_approver', 'l2_approver']
