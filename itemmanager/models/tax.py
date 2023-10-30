from django.db import models

class UserProfile(models.Model):
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    exemptions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_liability = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
