from django.db import transaction
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reservation.models import Department, Employee
from reservation.serializers import (
    EmployeeDepartmentUpdateSerializer,
    EmployeeSerializer,
)


# @api_view(["GET"])
# def get_all(request):
#     employee = Employee.objects.all()
#     serializer = EmployeeSerializer(employee, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_all(request):
    employee = get_list_or_404(Employee)
    serializer = EmployeeSerializer(employee, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get(request, pk):
    # Try to get the employee or return 404 if not found
    employee = get_object_or_404(Employee, pk=pk)
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    # Try to get the employee or return 404 if not found
    employee = get_object_or_404(
        Employee.objects.prefetch_related(
            "approvals",
            "immediate_head_approvals",
            "person_in_charge_approvals",
            "managed_facilities",
        ),
        user=user,
    )
    serializer = EmployeeSerializer(employee)
    return Response(serializer.data)


@api_view(["PATCH"])
# Add appropriate permissions as needed
# @permission_classes([])
def update_employees(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # Note 'partial=True' to allow partial updates
    serializer = EmployeeSerializer(employee, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
# Ensure only authenticated users can access this view
# @permission_classes([IsAuthenticated])
def update_employees_department(request):
    serializer = EmployeeDepartmentUpdateSerializer(data=request.data)
    if serializer.is_valid():
        employee_ids = serializer.validated_data["employee_ids"]
        department_id = serializer.validated_data["department_id"]
        department = Department.objects.get(id=department_id)

        # Update the department for all specified employees
        Employee.objects.filter(id__in=employee_ids).update(department=department)
        Employee.objects.filter(id__in=employee_ids).update(
            immediate_head=department.immediate_head
        )

        return Response(
            {"message": "Employees' department updated successfully"},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
