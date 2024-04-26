from rest_framework import viewsets
from reservation.models import Department
from reservation.serializers import DepartmentSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = DepartmentSerializer

    def get_queryset(self):
        queryset = Department.objects.all()
        superior_id = self.request.query_params.get('superior')
        if superior_id is not None:
            queryset = queryset.filter(superior_id=superior_id)
        return queryset