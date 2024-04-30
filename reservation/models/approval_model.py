from django.db import models
from reservation.models.event_model import Event
from reservation.models.employee_model import Employee


class Approval(models.Model):
    event = models.OneToOneField(
        Event, on_delete=models.CASCADE, related_name='approval')
    applicant = models.ForeignKey(
        Employee, related_name='approvals', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), (
        'approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    # Indicates whether the event is approved
    applicant_superior_approved = models.BooleanField(default=False)
    # Indicates whether the event is approved
    facility_authority_approved = models.BooleanField(default=False)
    # Indicates whether the event is approved
    admin_approved = models.BooleanField(default=False)

    def approve_by_l1(self, user):
        if user == self.l1_approver:
            self.applicant_superior_approved = True
            self.check_if_approved()

    def revoke_by_l1(self, user):
        if user == self.l1_approver:
            self.applicant_superior_approved = False
            self.check_if_approved()

    def approve_by_l2(self, user):
        if user == self.l2_approver:
            self.facility_authority_approved = True
            self.check_if_approved()

    def revoke_by_l2(self, user):
        if user == self.l1_approver:
            self.facility_authority_approved = False
            self.check_if_approved()

    def approve_by_admin(self, user):
        if user.is_admin == True:
            self.facility_authority_approved = True
            self.check_if_approved()

    def revoke_by_admin(self, user):
        if user == self.l1_approver:
            self.admin_approved = False
            self.check_if_approved()

    def check_if_approved(self):
        if self.l1_approver and self.l2_approver and self.admin_approved:
            self.status = 'approved'
            self.event.status = 2
        self.save()

    @property
    def l1_approver(self):
        return self.applicant.immediate_head

    @property
    def l2_approver(self):
        return self.event.reserved_facility.person_in_charge

    def __str__(self):
        return f"Approval for {self.event.event_name} by {self.applicant} status: {self.status}"
