from django.db import models

# Create your models here.
from django.db import models

class AnalysisRecord(models.Model):
    exercise = models.CharField(max_length=100)
    risk_percent = models.IntegerField()
    fault = models.CharField(max_length=200)
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.exercise} - {self.risk_percent}%"
