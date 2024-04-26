from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reservation.models.department_model import Department
from reservation.serializers.department_serializer import DepartmentSerializer


@api_view(["POST"])
def poem_create(request):
    serializer = DepartmentSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
def poem_list(request):
    department = Department.objects.all()
    serializer = DepartmentSerializer(data=request.data)
    return Response(serializer.data)


@api_view(["DELETE"])
def poem_delete(request, pk):
    department = Department.objects.get(id=pk)
    department.delete()

    return Response("Item Successfully deleted.")
