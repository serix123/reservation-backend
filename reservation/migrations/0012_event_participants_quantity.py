# Generated by Django 4.2.11 on 2024-05-04 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0011_alter_notification_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='participants_quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
