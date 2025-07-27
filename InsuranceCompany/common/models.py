from django.db import models

from InsuranceCompany.policies.models import Policy


# Create your models here.

class Car(models.Model):
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    price = models.IntegerField()
    policy = models.ForeignKey(
        Policy,
        on_delete=models.CASCADE,
        editable=False,
    )




