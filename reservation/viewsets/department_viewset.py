from rest_framework import viewsets
from reservation.models import Department
from reservation.serializers import DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        queryset = Department.objects.all()
        immediate_head_id = self.request.query_params.get('immediate_head')
        if immediate_head_id is not None:
            queryset = queryset.filter(immediate_head_id=immediate_head_id)
        return queryset