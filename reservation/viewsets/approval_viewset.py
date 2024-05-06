from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from reservation.models import Approval, Employee
from reservation.serializers import ApprovalSerializer


class ApprovalViewSet(viewsets.ModelViewSet):
    queryset = Approval.objects.all()
    serializer_class = ApprovalSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the approvals
        for the currently authenticated user if they are a immediate_head_approver.
        """
        queryset = self.queryset
        immediate_head_approver = self.request.query_params.get(
            "immediate_head_approver")
        person_in_charge_approver = self.request.query_params.get(
            "person_in_charge_approver")
        slip_number = self.request.query_params.get(
            "slip_number")

        # requesitioner = self.request.query_params.get("requesitioner")
        # if requesitioner:
        #     queryset = queryset.filter(
        #         requesitioner=requesitioner)

        if immediate_head_approver is not None:
            queryset = queryset.filter(
                immediate_head_approver=immediate_head_approver)
            return queryset

        if person_in_charge_approver is not None:
            queryset = queryset.filter(
                person_in_charge_approver=person_in_charge_approver)
            return queryset

        if slip_number is not None:
            queryset = queryset.filter(
                slip_number=slip_number)
            return queryset

        user = self.request.user
        employee = Employee.objects.get(user=user)
        queryset = queryset.filter(requesitioner=employee)
        return queryset
