# Generated by Django 4.2.11 on 2024-05-06 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0015_approval_admin_update_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='facilities_images/'),
        ),
    ]