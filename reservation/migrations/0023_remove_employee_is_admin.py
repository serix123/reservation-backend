# Generated by Django 4.2.11 on 2024-05-27 12:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0022_employee_is_admin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='is_admin',
        ),
    ]
