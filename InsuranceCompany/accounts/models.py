from django.db import models

# Create your models here.

from django.contrib.auth import models as auth_models, get_user_model
from django.db import models
from InsuranceCompany.accounts.managers import AppUserManager


# Create your models here.

class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(unique=True, null=False, blank=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AppUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='групи',
        blank=True,
        help_text='Групите, към които принадлежи потребителят.',
        related_name="appuser_groups",
        related_query_name="appuser",
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='права на потребителя',
        blank=True,
        help_text='Специфични права за този потребител.',
        related_name="appuser_permissions",
        related_query_name="appuser",
    )

    class Meta:
        swappable = 'AUTH_USER_MODEL'

    def __str__(self):
        return self.email


UserModel = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def get_profile_name(self):
        if self.first_name and self.last_name:
            return f'{self.first_name} {self.last_name}'
        elif self.first_name or self.last_name:
            return self.first_name or self.last_name
        else:
            return 'Anonymous user'
