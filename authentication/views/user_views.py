from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from authentication.models import User
from authentication.serializers import UserSerializer, ResidentRegistrationSerializer, StaffRegistrationSerializer, AdminUserUpdateSerializer


@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.create()
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def register_admin(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.create_superuser()
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def register_employee(request):
    user = request.user
    serializer = UserSerializer(
        data=request.data, context={'request': request})
    if serializer.is_valid():
        user = serializer.create_employee_and_assign()
        if user:
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update(request, pk):
    try:
        user = User.objects.get(id=pk)
    except User.DoesNotExist:
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = UserSerializer(instance=user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResidentRegistrationView(CreateAPIView):
    serializer_class = ResidentRegistrationSerializer
    permission_classes = [AllowAny]


class StaffRegistrationView(CreateAPIView):
    serializer_class = StaffRegistrationSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        if not self.request.user.is_superuser:
            return Response(
                {"error": "Only superadmins can create staff accounts"},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer.save()


class AdminUserViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]

    @action(detail=True, methods=['put', 'patch'])
    def permissions(self, request, pk=None):
        """Update user staff/superuser status (Admin only)"""
        target_user = get_object_or_404(User, pk=pk)

        if target_user == request.user:
            return Response(
                {"error": "Cannot modify your own permissions"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = AdminUserUpdateSerializer(
            target_user,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
