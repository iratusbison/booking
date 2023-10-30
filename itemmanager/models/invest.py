# models.py
from django.db import models
from datetime import date
from math import pow
from decimal import Decimal

class InSection(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Investment(models.Model):
    section = models.ForeignKey(InSection, on_delete=models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_approved = models.BooleanField(default=False)
    description = models.TextField(blank=True, null=True)

    # Add a field to specify the compounding frequency
    COMPOUND_CHOICES = [
        ('Annual', 'Annual'),
        ('Quarterly', 'Quarterly'),
        ('HalfYearly', 'Half-Yearly'),
    ]
    compound_frequency = models.CharField(
        max_length=20,
        choices=COMPOUND_CHOICES,
        default='Annual',  # Set a default value
    )


    def calculate_interest(self):
        # Calculate the number of days between start_date and end_date
        days_active = (self.end_date - self.start_date).days

        # Convert the principal and rate to Decimal
        principal = Decimal(str(self.amount))
        rate = Decimal(str(self.interest_rate)) / 100  # Convert the rate to a Decimal and a fraction (e.g., 0.05 for 5%)

        # Calculate interest with compounding using the formula: A = P(1 + r/n)^(nt)
        if self.compound_frequency == 'Annual':
            n = 1  # Annual compounding
        elif self.compound_frequency == 'Quarterly':
            n = 4  # Quarterly compounding (4 times a year)
        elif self.compound_frequency == 'HalfYearly':
            n = 2  # Half-yearly compounding (2 times a year)
        else:
            n = 1  # Default to annual compounding if the frequency is not recognized

        # Convert Decimal values back to float for use with pow
        principal = float(principal)
        rate = float(rate)

        # Calculate interest
        amount = Decimal(principal * pow(1 + rate / n, n * days_active / 365) - principal)

        return amount




class InPayment(models.Model):
    investment = models.ForeignKey(Investment, on_delete=models.CASCADE, null=True)
    INSTALLMENT = 'Installment'
    WHOLE_AMOUNT = 'Whole Amount'
    PAYMENT_CHOICES = [
        (INSTALLMENT, 'Installment'),
        (WHOLE_AMOUNT, 'Whole Amount'),
    ]
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    payment_date = models.DateField()
    payment_type = models.CharField(
        max_length=20,
        choices=PAYMENT_CHOICES,
        default=INSTALLMENT,
    )
