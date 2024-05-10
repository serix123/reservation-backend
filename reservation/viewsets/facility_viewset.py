from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from reservation.models import Facility
from reservation.serializers import FacilitySerializer


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all().prefetch_related('events')
    serializer_class = FacilitySerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)
