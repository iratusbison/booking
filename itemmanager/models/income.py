
from django.db import models


class IncSection(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Income(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    date = models.DateField()
    reserver = models.CharField(max_length=50, null=True)
    bride = models.CharField(max_length=50,null=True)
    groom = models.CharField(max_length= 50, null=True)
    reserver_address = models.CharField(max_length=500, null=True)
    reserver_phone = models.BigIntegerField(null=True)
    reserver_aadhar = models.BigIntegerField(null=True)
    checkin_datetime = models.DateTimeField(null=True)  
    checkout_datetime = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, choices=[("Pending", "Pending"), ("Completed", "Completed")], null = True)
    incsection = models.ForeignKey(IncSection, on_delete=models.CASCADE, null=True)

def __str__(self):
        return self.description


class MonthlyIncome(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
