from rest_framework import serializers

from reservation.models import Department, Employee


class DepartmentSerializer(serializers.ModelSerializer):

    superior = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), allow_null=True
    )

    class Meta:
        model = Department
        fields = "__all__"
