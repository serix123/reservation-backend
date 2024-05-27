# views.py
import csv
import io
from authentication.models import User
from rest_framework import status
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from authentication.serializers import CSVUploadSerializer, UserSerializer

DEFAULT_PASSWORD = 'pnMGgxsG1P3MKGk'


@api_view(['POST'])
@parser_classes([MultiPartParser, FormParser])
def upload_csv_create_users(request):
    serializer = CSVUploadSerializer(data=request.data)
    if serializer.is_valid():
        file = serializer.validated_data['file']
        if file is not None and not file.name.endswith('.csv'):
            return Response({'error': 'Invalid file format. Please upload a CSV file.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            data_set = file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            reader = csv.reader(io_string)
            data_list = []
            for row in reader:
                email = row[0]
                first_name = row[1]
                last_name = row[2]
                user_data = {
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "password": DEFAULT_PASSWORD,
                    "password2": DEFAULT_PASSWORD
                }
                print(user_data)
                if not User.objects.filter(email=email).exists():
                    serializer = UserSerializer(data=user_data)
                    if serializer.is_valid():
                        user = serializer.create()
                        if user:
                            data_list.append(serializer.data)
            return Response({'message': 'Users created successfully.', 'data': data_list}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
