from decimal import Decimal

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from datetime import date

from InsuranceCompany.policies.models import Discount, InsurancePolicy


# Create your models here.

class Car(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='car_user')
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.make} {self.model} {self.year}"


class Offer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Чакаща'),
        ('accepted', 'Приета'),
        ('rejected', 'Отхвърлена'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    insurance_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Застрахователна сума"
    )
    discounts = models.ManyToManyField(Discount, blank=True, related_name="offers")
    applied_discounts_text = models.TextField(blank=True, verbose_name="Приложени отстъпки")
    premium = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )
    related_name = 'offers'
    created_policy = models.OneToOneField(InsurancePolicy, on_delete=models.CASCADE, null=True,
                                          related_name='offer_to_policy')

    def accept(self):
        self.status = 'accepted'
        self.save()

    def reject(self):
        self.status = 'rejected'
        self.save()

    def __str__(self):
        return f"Оферта #{self.id} за {self.car} ({self.get_status_display()})"
