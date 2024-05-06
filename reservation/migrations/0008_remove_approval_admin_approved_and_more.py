# Generated by Django 4.2.11 on 2024-05-03 19:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_approval_immediate_head_approver_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='approval',
            name='admin_approved',
        ),
        migrations.RemoveField(
            model_name='approval',
            name='immediate_head_approved',
        ),
        migrations.RemoveField(
            model_name='approval',
            name='person_in_charge_approved',
        ),
        migrations.AddField(
            model_name='approval',
            name='admin_status',
            field=models.IntegerField(choices=[(-1, 'Rejected'), (0, 'No Decision'), (1, 'Approved')], default=0),
        ),
        migrations.AddField(
            model_name='approval',
            name='immediate_head_status',
            field=models.IntegerField(choices=[(-1, 'Rejected'), (0, 'No Decision'), (1, 'Approved')], default=0),
        ),
        migrations.AddField(
            model_name='approval',
            name='person_in_charge_status',
            field=models.IntegerField(choices=[(-1, 'Rejected'), (0, 'No Decision'), (1, 'Approved')], default=0),
        ),
    ]