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
        for the currently authenticated user if they are a superior.
        """

        # applicant = self.request.query_params.get("applicant")
        l1_approver = self.request.query_params.get("superior")
        l2_approver = self.request.query_params.get("person_in_charge")

        # if applicant:
        #     queryset = queryset.filter(
        #         applicant=applicant)

        if l1_approver:
            queryset = queryset.filter(
                l1_approver=l1_approver)
            return queryset

        if l2_approver:
            queryset = queryset.filter(
                l2_approver=l2_approver)
            return queryset

        user = self.request.user
        employee = Employee.objects.get(user=user)
        return Approval.objects.filter(applicant=employee)
