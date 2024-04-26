from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reservation.models import Department
from reservation.serializers import DepartmentSerializer


@api_view(["POST"])
def INSERT(request):
    serializer = DepartmentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)


@api_view(["GET"])
def GET_ALL(request):
    department = Department.objects.all()
    serializer = DepartmentSerializer(department, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def GET(request, pk):
    department = Department.objects.get(id=pk)
    serializer = DepartmentSerializer(department, many=False)
    return Response(serializer.data)


@api_view(["DELETE"])
def DELETE(request, pk):
    department = Department.objects.get(id=pk)
    department.delete()
    return Response("Item Successfully deleted.")


@api_view(["POST"])
def poem_update(request, pk):
    department = Department.objects.get(id=pk)
    serializer = DepartmentSerializer(instance=department, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
