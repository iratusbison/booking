from django.db import models


class IncSection(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Income(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    incsection = models.ForeignKey(IncSection, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description
