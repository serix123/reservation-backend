from rest_framework import serializers

from reservation.models.employee_model import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('employee_type')
