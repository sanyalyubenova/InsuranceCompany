from django import forms
from django.contrib.auth.models import User

from InsuranceCompany.policies.models import InsurancePolicy, Claim, Discount


class CalculatorForm(forms.Form):
    pass

class PolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = ['user', 'car', 'insurance_amount']

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['policy', 'description', 'status']

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['percentage',]

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']