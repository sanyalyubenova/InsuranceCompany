from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from InsuranceCompany.accounts.models import Profile

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile for new users"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=UserModel)
def save_user_profile(sender, instance, **kwargs):
    """Save the profile when user is saved"""
    try:
        instance.profile.save()
    except Profile.DoesNotExist:
        Profile.objects.create(user=instance) 