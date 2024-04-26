from rest_framework import serializers

from reservation.models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ("immediate_head", "department")
