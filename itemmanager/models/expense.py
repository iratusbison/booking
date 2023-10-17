from django.db import models


class ESection(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Expense(models.Model):
    description = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    esection = models.ForeignKey(ESection, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.description
