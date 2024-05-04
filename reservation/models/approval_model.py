from django.db import models
from reservation.models.event_model import Event
from reservation.models.employee_model import Employee


class Approval(models.Model):
    event = models.OneToOneField(
        Event, on_delete=models.CASCADE, related_name='approval')
    requesitioner = models.ForeignKey(
        Employee, related_name='approvals', on_delete=models.CASCADE)
    immediate_head_approver = models.ForeignKey(
        Employee, related_name='immediate_head_approvals', on_delete=models.CASCADE)
    person_in_charge_approver = models.ForeignKey(
        Employee, related_name='person_in_charge_approvals', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), (
        'approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

    # Indicates whether the event is approved
    # immediate_head_approved = models.BooleanField(default=False)
    immediate_head_status = models.IntegerField(
        default=0, choices=[(-1, 'Rejected'), (0, 'No Decision'), (1, 'Approved')])

    # Indicates whether the event is approved
    # person_in_charge_approved = models.BooleanField(default=False)
    person_in_charge_status = models.IntegerField(
        default=0, choices=[(-1, 'Rejected'), (0, 'No Decision'), (1, 'Approved')])

    # Indicates whether the event is approved
    # admin_approved = models.BooleanField(default=False)
    admin_status = models.IntegerField(
        default=0, choices=[(-1, 'Rejected'), (0, 'No Decision'), (1, 'Approved')])

    def approve_by_immediate_head(self, employee):
        if employee == self.immediate_head_approver:
            self.immediate_head_status = 1
            self.check_if_approved()

    def revoke_by_immediate_head(self, employee):
        if employee == self.immediate_head_approver:
            self.immediate_head_status = 0
            self.check_if_approved()

    def reject_by_immediate_head(self, employee):
        if employee == self.immediate_head_approver:
            self.immediate_head_status = -1
            self.check_if_approved()

    def approve_by_person_in_charge(self, employee):
        if employee == self.person_in_charge_approver:
            self.person_in_charge_status = 1
            self.check_if_approved()

    def revoke_by_person_in_charge(self, employee):
        if employee == self.person_in_charge_approver:
            self.person_in_charge_status = 0
            self.check_if_approved()

    def reject_by_person_in_charge(self, employee):
        if employee == self.person_in_charge_approver:
            self.person_in_charge_status = -1
            self.check_if_approved()

    def approve_by_admin(self, employee):
        if employee.is_admin == True:
            self.admin_status = 1
            self.check_if_approved()

    def revoke_by_admin(self, employee):
        if employee.is_admin == True:
            self.admin_status = 0
            self.check_if_approved()

    def reject_by_admin(self, employee):
        if employee.is_admin == True:
            self.admin_status = -1
            self.check_if_approved()

    def check_if_approved(self):
        if self.immediate_head_status and self.person_in_charge_status and self.admin_status:
            self.status = 'approved'
            self.event.status = "confirmed"
            self.event.approve_event()
        self.save()

    @property
    def immediate_head_approval(self):
        """Return a human-readable status."""
        if self.immediate_head_status == 1:
            return "Approved"
        elif self.immediate_head_status == -1:
            return "No Decision"
        return "None"

    @property
    def person_in_charge_approval(self):
        """Return a human-readable status."""
        if self.person_in_charge_status == 1:
            return "Approved"
        elif self.person_in_charge_status == -1:
            return "No Decision"
        return "None"

    @property
    def admin_approval(self):
        """Return a human-readable status."""
        if self.admin_status == 1:
            return "Approved"
        elif self.admin_status == -1:
            return "No Decision"
        return "None"

    def __str__(self):
        return f"Approval for {self.event.event_name} ({self.status})"
