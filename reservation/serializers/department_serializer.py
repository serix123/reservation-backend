from rest_framework import serializers

from reservation.models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):

    immediate_head = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,  # Not required for updates
        allow_null=True,  # Allows the immediate_head to be null
    )

    class Meta:
        model = Department
        fields = "__all__"
        # Not required for updates
        extra_kwargs = {"name": {"required": False}}
