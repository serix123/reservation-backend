from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reservation.models import Approval
from reservation.serializers import ApprovalSerializer


@api_view(["GET"])
def get_all(request):
    approval = Approval.objects.all()
    serializer = ApprovalSerializer(approval, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["GET"])
def get_approver_approvals(request):
    user = request.user
    approval = Approval.objects.all()
    serializer = ApprovalSerializer(approval, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_by_superior(request, pk):
    approval = Approval.objects.get(pk=pk)
    if request.user == approval.l1_approver:
        approval.approve_by_l1(request.user)
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_by_person_in_charge(request, pk):
    approval = Approval.objects.get(pk=pk)
    if request.user == approval.l2_approver:
        approval.approve_by_l2(request.user)
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def revoke_by_superior(request, pk):
    approval = Approval.objects.get(pk=pk)
    if request.user == approval.l1_approver:
        approval.revoke_by_l1(request.user)
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def revoke_by_person_in_charge(request, pk):
    approval = Approval.objects.get(pk=pk)
    if request.user == approval.l2_approver:
        approval.revoke_by_l2(request.user)
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
