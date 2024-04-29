from rest_framework import serializers
from reservation.models import Equipment


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"  # Exposes all fields from the Equipment model
