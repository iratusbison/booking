# Generated by Django 3.2.7 on 2024-02-10 04:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmanager', '0046_booking_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='persons',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
