from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'InsuranceCompany.accounts'

    def ready(self):
        import InsuranceCompany.accounts.signals
