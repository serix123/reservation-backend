from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models import User
from reservation.models import Department


class Employee(models.Model):
    # class EmployeeTypes(models.TextChoices):
    #     EMPLOYEE = "1", "Employee"
    #     SUPERIOR = "2", "Superior"
    #     FACILITY_SUPERIOR = "3", "Facility Superior"
    #     ADMIN = "4", "Admin"

    # employee_type = models.CharField(
    #     max_length=2,
    #     choices=EmployeeTypes.choices,
    #     default=EmployeeTypes.EMPLOYEE,
    # )

    first_name = models.CharField(max_length=100, default="first_name")
    last_name = models.CharField(max_length=100, default="last_name")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    immediate_head = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, related_name="subordinates"
    )
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    REQUIRED_FIELDS = ["user"]

    # def __str__(self):
    #     return  self.user.username
    @property
    def is_admin(self):
        return self.user.is_superuser

    @property
    def date_joined(self):
        return self.user.date_joined

    def __str__(self):
        return self.first_name + " " + self.last_name


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Employee.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.employee.save()
