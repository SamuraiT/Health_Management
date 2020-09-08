from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
EXERCISE = (('N/A', 'Exercise'),('Yes', 'Yes'), ('No', 'No'))

class HealthApp(models.Model):
    postdate = models.DateField()
    weight = models.FloatField(max_length=100)
    steps = models.IntegerField()
    exercise = models.CharField(max_length=10, choices=EXERCISE)
    notes = models.TextField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.SET_NULL,
        null=True
    )
    def __str__(self):
        return str(self.postdate)
