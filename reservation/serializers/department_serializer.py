from rest_framework import serializers

from reservation.models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):

    superior = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(),
        required=False,  # Not required for updates
        allow_null=True,  # Allows the superior to be null
    )

    class Meta:
        model = Department
        fields = "__all__"
        extra_kwargs = {"name": {"required": False}}  # Not required for updates
