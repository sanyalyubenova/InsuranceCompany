from django import forms

from InsuranceCompany.common.models import Offer, Car


class OfferCreateForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['insurance_amount']

    make = forms.CharField(max_length=100, label="Марка")
    model = forms.CharField(max_length=100, label="Модел")
    year = forms.IntegerField(label="Година на производство")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['insurance_amount'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Въведи застрахователна сума'})
        self.fields['make'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Въведи марка'})
        self.fields['model'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Въведи модел'})
        self.fields['year'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Въведи година на производство'})



class OfferEditForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['insurance_amount', 'status', 'discounts', 'premium']

        widgets = {
            'insurance_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'discounts': forms.Select(attrs={'class': 'form-control'}),
            'premium': forms.NumberInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'insurance_amount': 'Застрахователна сума',
            'status': 'Статус',
            'discounts': 'Отстъпки',
            'premium': 'Премия',
        }


class CarCreateForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year']
        labels = {
            'make': 'Марка',
            'model': 'Модел',
            'year': 'Година на производство',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['make'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Въведи марка'})
        self.fields['model'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Въведи модел'})
        self.fields['year'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Въведи година на производство'})


class CarEditForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ['make', 'model', 'year']
        labels = {
            'make': 'Марка',
            'model': 'Модел',
            'year': 'Година на производство',
        }
        widgets = {
            'make': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Въведи марка'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Въведи модел'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Въведи година на производство'}),
        }
