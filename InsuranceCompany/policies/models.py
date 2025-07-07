from django.db import models

from InsuranceCompany.clients.models import Client


class Policy(models.Model):
    # policy_number = TO-DO
    insurance_value = models.IntegerField()
    insurance_price = models.FloatField()
    start_date = models.DateField()
    end_date = models.DateField()
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        editable=False,
    )
