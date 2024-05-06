from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from authentication.models import User
from reservation.models import Approval, Employee
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
def approve_by_immediate_head(request, slip_number):
    approval = Approval.objects.get(slip_number=slip_number)
    employee = Employee.objects.get(user=request.user)
    if employee == approval.immediate_head_approver:
        approval.approve_by_immediate_head(employee)
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def revoke_by_immediate_head(request, slip_number):
    approval = Approval.objects.get(slip_number=slip_number)
    employee = Employee.objects.get(user=request.user)
    if employee == approval.immediate_head_approver:
        approval.revoke_by_immediate_head(employee)
        return Response({'status': 'revoked'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_by_immediate_head(request, slip_number):
    approval = Approval.objects.get(slip_number=slip_number)
    employee = Employee.objects.get(user=request.user)
    if employee == approval.immediate_head_approver:
        approval.reject_by_immediate_head(employee)
        return Response({'status': 'rejected'}, status=status.HTTP_200_OK)
    return Response(employee, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def approve_by_person_in_charge(request, slip_number):
    approval = Approval.objects.get(slip_number=slip_number)
    employee = Employee.objects.get(user=request.user)
    if employee == approval.person_in_charge_approver:
        approval.approve_by_person_in_charge(employee)
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def revoke_by_person_in_charge(request, slip_number):
    approval = Approval.objects.get(slip_number=slip_number)
    employee = Employee.objects.get(user=request.user)
    if employee == approval.person_in_charge_approver:
        approval.revoke_by_person_in_charge(employee)
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def reject_by_person_in_charge(request, slip_number):
    approval = Approval.objects.get(slip_number=slip_number)
    employee = Employee.objects.get(user=request.user)
    if employee == approval.person_in_charge_approver:
        approval.reject_by_person_in_charge(employee)
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def approve_by_admin(request, slip_number):
    approval = Approval.objects.get(slip_number=slip_number)
    employee = Employee.objects.get(user=request.user)
    if employee.is_admin == True:
        approval.approve_by_admin(employee=employee)
        return Response({'status': 'approved'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def revoke_by_admin(request, slip_number):
    approval = Approval.objects.get(slip_number=slip_number)
    employee = Employee.objects.get(user=request.user)
    if employee.is_admin == True:
        approval.revoke_by_admin(employee=employee)
        return Response({'status': 'revoked'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def reject_by_admin(request, slip_number):
    approval = Approval.objects.get(slip_number=slip_number)
    employee = Employee.objects.get(user=request.user)
    if employee.is_admin == True:
        approval.reject_by_admin(employee=employee)
        return Response({'status': 'rejected'}, status=status.HTTP_200_OK)
    return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
