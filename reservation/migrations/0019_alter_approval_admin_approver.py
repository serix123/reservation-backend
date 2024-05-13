# Generated by Django 4.2.11 on 2024-05-13 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0018_approval_admin_approver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approval',
            name='admin_approver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='admin_approvals', to='reservation.employee'),
        ),
    ]
