from rest_framework import serializers
from reservation.models import Department, Employee
from reservation.serializers.approval_serializer import ApprovalSerializer
from reservation.serializers.facility_serializer import FacilitySerializer


class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()
    approvals = ApprovalSerializer(many=True, read_only=True)
    immediate_head_approvals = ApprovalSerializer(many=True, read_only=True)
    person_in_charge_approvals = ApprovalSerializer(many=True, read_only=True)
    managed_facilities = FacilitySerializer(many=True, read_only=True)
    immediate_head_details = serializers.SerializerMethodField()
    department_details = serializers.SerializerMethodField()
    is_admin = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_admin",
            "user",
            "immediate_head",
            "immediate_head_details",
            "department",
            "department_details",
            "approvals",
            "immediate_head_approvals",
            "person_in_charge_approvals",
            "managed_facilities",
        ]
        extra_kwargs = {
            "user": {"required": False},
            "approvals": {"required": False},
            "immediate_head_approvals": {"required": False, },
            "person_in_charge_approvals": {"required": False, },
            "managed_facilities": {"required": False, },
        }

    def get_immediate_head_details(self, obj):
        if obj.immediate_head:
            return {
                "id": obj.immediate_head.id,
                "first_name": obj.immediate_head.first_name,
                "last_name": obj.immediate_head.last_name,
            }
        return None

    def get_department_details(self, obj):
        if obj.department:
            return {
                "id": obj.department.id,
                "name": obj.department.name,
            }
        return None

    def get_email(self, obj):
        if obj.user:
            return obj.user.email
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
