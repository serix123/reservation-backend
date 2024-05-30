import json
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from reservation.models import Facility
from reservation.serializers import FacilitySerializer


class FacilityViewSet(viewsets.ModelViewSet):
    queryset = Facility.objects.all().prefetch_related('events')
    serializer_class = FacilitySerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def create(self, request, *args, **kwargs):
        # Extract and parse the JSON data from the 'data' field in the multipart form
        data = request.data.get("data")
        if data:
            try:
                json_data = json.loads(
                    data
                )  # Convert JSON string back to Python dictionary
            except json.JSONDecodeError:
                return Response(
                    {"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Handle file if included
        if "image" in request.FILES:
            json_data["image"] = request.FILES["image"]

        print(json_data)
        serializer = self.get_serializer(data=json_data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()

        # Extract and parse the JSON data from the 'data' field in the multipart form
        data = request.data.get("data")
        if data:
            try:
                # Convert JSON string back to Python dictionary
                json_data = json.loads(data)
            except json.JSONDecodeError:
                return Response(
                    {"error": "Invalid JSON data"}, status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "No data provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Handle file if included
        if "image" in request.FILES:
            json_data["image"] = request.FILES["image"]

        print(json_data)
        serializer = self.get_serializer(
            instance, data=json_data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
