# Generated by Django 4.2.11 on 2024-05-13 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0017_event_event_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='approval',
            name='admin_approver',
            field=models.ForeignKey(default=33, on_delete=django.db.models.deletion.CASCADE, related_name='admin_approvals', to='reservation.employee'),
            preserve_default=False,
        ),
    ]
