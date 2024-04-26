from django.db import models


from reservation.models import Employee


class Facility(models.Model):
    name = models.CharField(max_length=100)
    # location_description = models.TextField()
    # capacity = models.IntegerField()
    person_in_charge = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        related_name="managed_facilities",
    )

    def __str__(self):
        return self.name


# class Approval(models.Model):
#     request = models.ForeignKey(
#         ReservationRequest, on_delete=models.CASCADE, related_name="approvals"
#     )
#     approver = models.ForeignKey(
#         Employee, on_delete=models.CASCADE, related_name="given_approvals"
#     )
#     approval_type = models.CharField(
#         max_length=20,
#         choices=[
#             ("Department Superior", "Department Superior"),
#             ("Facility Manager", "Facility Manager"),
#         ],
#     )
#     status = models.CharField(
#         max_length=10,
#         choices=[
#             ("Pending", "Pending"),
#             ("Approved", "Approved"),
#             ("Rejected", "Rejected"),
#         ],
#     )
#     date_approved = models.DateTimeField(null=True, blank=True)

#     def __str__(self):
#         return f"{self.approval_type} by {self.approver.name} for {self.request}"
