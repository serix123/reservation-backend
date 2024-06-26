from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reservation.models import Equipment
from reservation.serializers import EquipmentSerializer


@api_view(["GET"])
def get_all_equipments(request):
    department = Equipment.objects.all()
    serializer = EquipmentSerializer(department, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
