from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from residence.models import Residence
from residence.serializers import ResidenceSerializer, CreateResidenceSerializer


class ResidenceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateResidenceSerializer
        return ResidenceSerializer

    def get_queryset(self):
        # Admins can see all, regular users only their own
        if self.request.user.is_staff:
            return Residence.objects.all()
        return Residence.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set first_name/last_name from user if not provided
        # user = self.request.user
        serializer.save(
            # first_name=serializer.validated_data.get(
            #     'first_name', user.first_name),
            # last_name=serializer.validated_data.get(
            #     'last_name', user.last_name)
        )
