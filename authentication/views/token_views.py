from rest_framework_simplejwt.views import TokenObtainPairView

from authentication.serializers.token_serializer import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
