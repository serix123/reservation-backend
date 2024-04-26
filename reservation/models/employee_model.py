from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from authentication.models.user_model import User
from reservation.models.department_model import Department


class Employee(models.Model):
    class EmployeeTypes(models.TextChoices):
        EMPLOYEE = '1', 'Employee'
        SUPERIOR = '2', 'Superior'
        FACILITY_SUPERIOR = '3', 'Facility Superior'
        ADMIN = '4', 'Admin'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    immediate_head = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, related_name='subordinates')
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True)

    employee_type = models.CharField(
        max_length=2,
        choices=EmployeeTypes.choices,
        default=EmployeeTypes.EMPLOYEE,
    )

    def __str__(self):
        return self.user.get_full_name() or self.user.username


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Employee.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.employee.save()
