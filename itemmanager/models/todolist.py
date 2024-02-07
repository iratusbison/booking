from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    start_date = models.DateField(null=True, blank=True)
    #due_date = models.DateField()
    #completion = models.PositiveIntegerField(choices=[(25, '25%'), (50, '50%'), (75, '75%'), (100, '100%')], default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.title
