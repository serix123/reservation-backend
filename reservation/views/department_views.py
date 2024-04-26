from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reservation.models import Department, Employee
from reservation.serializers import DepartmentSerializer


@api_view(["POST"])
def insert(request):
    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def get_all(request):
    department = Department.objects.all()
    serializer = DepartmentSerializer(department, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
def get(request, pk):
    department = Department.objects.get(id=pk)
    serializer = DepartmentSerializer(department, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def delete(request, pk):
    department = Department.objects.get(id=pk)
    department.delete()
    return Response("Item Successfully deleted.")


@api_view(["POST"])
def update(request, pk):
    department = Department.objects.get(id=pk)
    serializer = DepartmentSerializer(instance=department, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PATCH"])
@permission_classes([])  # Add appropriate permissions as needed
def update_department(request, pk):
    try:
        department = Department.objects.get(pk=pk)
    except Department.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    # Note 'partial=True' to allow partial updates
    serializer = DepartmentSerializer(department, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
# @permission_classes([])
def update_dept_head(request, pk):
    try:
        department = Department.objects.get(pk=pk)
    except Department.DoesNotExist:
        return Response(
            {"error": "Department not found"}, status=status.HTTP_404_NOT_FOUND
        )

    # Get the current superior before update
    old_superior = department.superior

    serializer = DepartmentSerializer(department, data=request.data)
    if serializer.is_valid():
        with transaction.atomic():
            department = serializer.save()  # Save the updated department

            new_superior = serializer.validated_data.get("superior")
            # If the superior has changed, update all employees in this department
            if old_superior != new_superior:
                Employee.objects.filter(
                    department=department, immediate_head=old_superior
                ).update(immediate_head=new_superior)

            return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
