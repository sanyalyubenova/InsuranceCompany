from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from InsuranceCompany.accounts.models import Profile

# Create your models here.

import random

class InsurancePolicy(models.Model):
    policy_number = models.CharField(max_length=10, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    car = models.OneToOneField('common.Car', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    insurance_amount = models.DecimalField(max_digits=10, decimal_places=2)
    offer = models.OneToOneField('common.Offer', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.policy_number:
            self.policy_number = f"POL-{random.randint(100000, 999999)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.policy_number}"

    def get_status_display(self):
        return "Активна" if self.is_active else "Неактивна"

class Discount(models.Model):
    DISCOUNT_TYPES = [
        ('LOYALTY', 'Лоялност'),
        ('SAFE_DRIVER', 'Без щети'),
        ('MULTI_POLICY', 'Множествени полици'),
    ]

    discount_type = models.CharField(max_length=12, choices=DISCOUNT_TYPES)
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    applicable_to = models.ManyToManyField(InsurancePolicy, blank=True)

    def __str__(self):
        return f"{self.discount_type} ({self.percentage}%)"

    def discount_percentage(self):
        return self.percentage / 100

class Claim(models.Model):
    CLAIM_STATUS = [
        ('PENDING', 'Чакаща'),
        ('APPROVED', 'Одобрена'),
        ('REJECTED', 'Отхвърлена'),
    ]

    policy = models.ForeignKey(InsurancePolicy, on_delete=models.CASCADE)
    claim_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=CLAIM_STATUS, default='PENDING')
    photos = models.ImageField(upload_to='claims/', blank=True)

    def __str__(self):
        return f"Claim #{self.id} - {self.policy.policy_number}"
