from rest_framework import viewsets
from reservation.models import Equipment
from reservation.serializers import EquipmentSerializer


class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned equipment to a given type, name, ID,
        or availability status, by filtering against query parameters in the URL.
        """
        queryset = self.queryset
        equipment_type = self.request.query_params.get("equipment_type")
        equipment_name = self.request.query_params.get("equipment_name")
        equipment_id = self.request.query_params.get("id")

        if type:
            queryset = queryset.filter(type__iexact=equipment_type)
        if equipment_name:
            queryset = queryset.filter(name__icontains=equipment_name)
        if equipment_id:
            queryset = queryset.filter(id=equipment_id)

        return queryset
