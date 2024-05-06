from rest_framework import serializers

from reservation.models import Department, Employee


class EmployeeSerializer(serializers.ModelSerializer):
    immediate_head_details = serializers.SerializerMethodField()
    department_details = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = ["id", "first_name", "last_name",
                  "immediate_head", 'immediate_head_details', "department", "department_details"]

    def get_immediate_head_details(self, obj):
        if obj.immediate_head:
            return {
                'id': obj.immediate_head.id,
                'first_name': obj.immediate_head.first_name,
                'last_name': obj.immediate_head.last_name,
            }
        return None

    def get_department_details(self, obj):
        if obj.department:
            return {
                'id': obj.department.id,
                'name': obj.department.name,
            }
        return None


class EmployeeDepartmentUpdateSerializer(serializers.Serializer):
    employee_ids = serializers.ListField(child=serializers.IntegerField())
    department_id = serializers.IntegerField()

    def validate_department_id(self, value):
        if not Department.objects.filter(id=value).exists():
            raise serializers.ValidationError(
                "This department does not exist.")
        return value

    def update(self, instance, validated_data):
        employee_ids = validated_data.get("employee_ids")
        department = Department.objects.get(
            id=validated_data.get("department_id"))
        employees = Employee.objects.filter(id__in=employee_ids)
        for employee in employees:
            employee.department = department
            employee.save()
        return instance

    def validate_employee_ids(self, value):
        if not Employee.objects.filter(id__in=value).exists():
            raise serializers.ValidationError(
                "One or more employee IDs are invalid.")
        return value
