from django.db import models

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=200)
    due_date = models.DateField()
    importance = models.IntegerField(default=5)
    estimated_hours = models.IntegerField(default=1)
    dependencies = models.JSONField(default=list, blank=True)

    