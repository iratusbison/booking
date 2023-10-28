# Generated by Django 4.0.6 on 2023-10-25 05:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmanager', '0028_income_status_delete_work'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthIncome',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
            ],
        ),
    ]