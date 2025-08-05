from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from InsuranceCompany.accounts.models import Profile, AppUser
from InsuranceCompany.common.models import Car, Offer
from InsuranceCompany.policies.models import InsurancePolicy, Claim, Discount


class Command(BaseCommand):
    help = 'Настройване на групи и разрешения'

    def handle(self, *args, **options):
        global group, perms
        clients_group, created = Group.objects.get_or_create(name='Clients')
        staff_group, created = Group.objects.get_or_create(name='Staff')
        superusers_group, created = Group.objects.get_or_create(name='Superusers')

        content_type = ContentType.objects.get_for_model(Group)
        add_group = Permission.objects.get(codename='add_group', content_type=content_type)
        change_group = Permission.objects.get(codename='change_group', content_type=content_type)
        delete_group = Permission.objects.get(codename='delete_group', content_type=content_type)
        view_group = Permission.objects.get(codename='view_group', content_type=content_type)

        content_type = ContentType.objects.get_for_model(Permission)
        add_permission = Permission.objects.get(codename='add_permission', content_type=content_type)
        change_permission = Permission.objects.get(codename='change_permission', content_type=content_type)
        delete_permission = Permission.objects.get(codename='delete_permission', content_type=content_type)
        view_permission = Permission.objects.get(codename='view_permission', content_type=content_type)

        content_type = ContentType.objects.get_for_model(Profile)
        add_profile = Permission.objects.get(codename='add_profile', content_type=content_type)
        change_profile = Permission.objects.get(codename='change_profile', content_type=content_type)
        delete_profile = Permission.objects.get(codename='delete_profile', content_type=content_type)
        view_profile = Permission.objects.get(codename='view_profile', content_type=content_type)

        content_type = ContentType.objects.get_for_model(AppUser)
        add_appuser = Permission.objects.get(codename='add_appuser', content_type=content_type)
        change_appuser = Permission.objects.get(codename='change_appuser', content_type=content_type)
        delete_appuser = Permission.objects.get(codename='delete_appuser', content_type=content_type)
        view_appuser = Permission.objects.get(codename='view_appuser', content_type=content_type)

        content_type = ContentType.objects.get_for_model(InsurancePolicy)
        add_policy = Permission.objects.get(codename='add_insurancepolicy', content_type=content_type)
        change_policy = Permission.objects.get(codename='change_insurancepolicy', content_type=content_type)
        delete_policy = Permission.objects.get(codename='delete_insurancepolicy', content_type=content_type)
        view_policy = Permission.objects.get(codename='view_insurancepolicy', content_type=content_type)

        content_type = ContentType.objects.get_for_model(Claim)
        add_claim = Permission.objects.get(codename='add_claim', content_type=content_type)
        change_claim = Permission.objects.get(codename='change_claim', content_type=content_type)
        delete_claim = Permission.objects.get(codename='delete_claim', content_type=content_type)
        view_claim = Permission.objects.get(codename='view_claim', content_type=content_type)

        content_type = ContentType.objects.get_for_model(Discount)
        add_discount = Permission.objects.get(codename='add_discount', content_type=content_type)
        change_discount = Permission.objects.get(codename='change_discount', content_type=content_type)
        delete_discount = Permission.objects.get(codename='delete_discount', content_type=content_type)
        view_discount = Permission.objects.get(codename='view_discount', content_type=content_type)

        content_type = ContentType.objects.get_for_model(Car)
        add_car = Permission.objects.get(codename='add_car', content_type=content_type)
        change_car = Permission.objects.get(codename='change_car', content_type=content_type)
        delete_car = Permission.objects.get(codename='delete_car', content_type=content_type)
        view_car = Permission.objects.get(codename='view_car', content_type=content_type)

        content_type = ContentType.objects.get_for_model(Offer)
        add_offer = Permission.objects.get(codename='add_offer', content_type=content_type)
        change_offer = Permission.objects.get(codename='change_offer', content_type=content_type)
        delete_offer = Permission.objects.get(codename='delete_offer', content_type=content_type)
        view_offer = Permission.objects.get(codename='view_offer', content_type=content_type)

        permissions_map = {
            'Clients': [
                 view_policy,
                 view_claim, change_claim, add_claim,
                 view_offer,
            ],

            'Staff': [
                 view_profile,  change_profile,
                 view_policy,   change_policy,   add_policy,
                 view_claim,    change_claim,    add_claim,    delete_claim,
                 view_discount, change_discount, add_discount, delete_discount,
                 view_car,      change_car,      add_car,
                 view_offer,    change_offer,    add_offer,
            ],

            'Superusers': [
                 view_group,      change_group,      add_group,      delete_group,
                 view_permission, change_permission, add_permission, delete_permission,
                 view_profile,    change_profile,    add_profile,    delete_profile,
                 view_appuser,    change_appuser,    add_appuser,    delete_appuser,
                 view_policy,     change_policy,     add_policy,     delete_policy,
                 view_claim,      change_claim,      add_claim,      delete_claim,
                 view_discount,   change_discount,   add_discount,   delete_discount,
                 view_car,        change_car,        add_car,        delete_car,
                 view_offer,      change_offer,      add_offer,      delete_offer,
            ],
        }

        for group_name, perms in permissions_map.items():
            group = Group.objects.get(name=group_name)
            current_perms = set(group.permissions.all())
            desired_perms = set(perms)

            for perm in desired_perms - current_perms:
                group.permissions.add(perm)

            for perm in current_perms - desired_perms:
                group.permissions.remove(perm)

            self.stdout.write(self.style.SUCCESS(f'Set permissions за {group_name}'))

        self.stdout.write(self.style.SUCCESS('Successfully set all permissions'))
