from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from medilab.models import MedicalRecord
from medilab.serializers import MedicalRecordSerializer


class MedicalRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling CRUD operations on Medical Records.
    Provides secure, context-aware access to medical record data.
    """
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Customize queryset based on user permissions.
        - Staff can see all records
        - Regular users can only see their own patient records
        """
        user = self.request.user
        if user.is_staff:
            return MedicalRecord.objects.all()

        # Assuming patient profile is linked to user
        return MedicalRecord.objects.filter(patient__user=user)

    @action(detail=False, methods=['GET'])
    def patient_records(self, request):
        """
        Custom action to retrieve medical records for the current user's patient profile.
        """
        try:
            # Assuming a patient profile exists for the current user
            records = MedicalRecord.objects.filter(patient__user=request.user)
            serializer = self.get_serializer(records, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'detail': str(e)}, status=400)
