from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.response import Response
from authentication.models import User
from authentication.permissions import IsAdminOrOfficer
from authentication.serializers import UserSerializer, ResidentRegistrationSerializer, StaffRegistrationSerializer, AdminUserUpdateSerializer, UserWithResidenceSerializer


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


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserWithResidenceSerializer
    permission_classes = [IsAdminOrOfficer]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['residence__role', 'is_staff', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['email', 'date_joined']
    ordering = ['-date_joined']

    def get_queryset(self):
        user = self.request.user

        # Superadmins see all users
        if user.is_superuser:
            return User.objects.all()

        # Officers only see residents
        return User.objects.filter(
            is_staff=False,
            is_superuser=False
        )


class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Simple viewset to return basic user information
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return the requesting user's data
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Convenience endpoint for getting current user's info"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
