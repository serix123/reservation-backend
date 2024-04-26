from django.db import models

from reservation.models import ( Facility, Employee)


class ReservationRequest(models.Model):
    facility = models.ForeignKey(Facility, on_delete=models.CASCADE, related_name='reservation_requests')
    requester = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reservation_requests')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')])
    date_requested = models.DateTimeField(auto_now_add=True)
    date_responded = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.facility.name} reserved by {self.requester.name}"