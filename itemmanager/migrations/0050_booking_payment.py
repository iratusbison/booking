# Generated by Django 3.2.7 on 2024-02-13 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmanager', '0049_auto_20240210_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='payment',
            field=models.CharField(choices=[('cash', 'Cash'), ('debit/credit_card', 'Debit/Credit_Card'), ('upi', 'UPI'), ('netbanking', 'NetBanking')], max_length=20, null=True),
        ),
    ]
