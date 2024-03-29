# Generated by Django 4.0.6 on 2024-02-07 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itemmanager', '0040_rdsection_remove_rd_period_months_rd_end_date_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('available', models.BooleanField(default=True)),
                ('unavailable', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=500, null=True)),
                ('phone', models.BigIntegerField(null=True)),
                ('aadhar', models.BigIntegerField(null=True)),
                ('email', models.EmailField(max_length=254, null=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('rooms', models.ManyToManyField(to='itemmanager.room')),
            ],
        ),
    ]
