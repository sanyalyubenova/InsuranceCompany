from django import forms
from django.contrib.auth.models import User

from InsuranceCompany.common.models import Offer
from InsuranceCompany.policies.models import InsurancePolicy, Claim, Discount


class CalculatorForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['insurance_amount']

    make = forms.CharField(max_length=100, label="Марка")
    model = forms.CharField(max_length=100, label="Модел")
    year = forms.IntegerField(label="Година на производство")


class PolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = ['start_date', 'end_date', 'price', 'insurance_amount', 'car', 'is_active']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'insurance_amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'car': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['policy', 'description', 'status']


class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['percentage', ]


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
