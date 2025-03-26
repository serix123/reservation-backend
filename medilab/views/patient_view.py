from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from medilab.models import Patient
from medilab.serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for handling CRUD operations on Patient models.
    Provides standard create, retrieve, update, and delete functionality.
    """
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    # Optional permission classes
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Customize queryset based on user permissions.
        Allows staff to see all patients, regular users to see only their own.
        """
        user = self.request.user
        if user.is_staff:
            return Patient.objects.all()
        return Patient.objects.filter(user=user)

    @action(detail=False, methods=['GET'])
    def my_profile(self, request):
        """
        Custom action to retrieve the current user's patient profile.
        """
        try:
            patient = Patient.objects.get(user=request.user)
            serializer = self.get_serializer(patient)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            return Response({'detail': 'No patient profile found.'}, status=404)
