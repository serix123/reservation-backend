# Generated by Django 4.2.11 on 2024-05-13 17:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0019_alter_approval_admin_approver'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approval',
            name='admin_approver',
        ),
    ]
