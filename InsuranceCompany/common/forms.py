from datetime import date

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
        self.fields['insurance_amount'].widget.attrs['class'] = 'form-control'
        self.fields['make'].widget.attrs['class'] = 'form-control'
        self.fields['model'].widget.attrs['class'] = 'form-control'
        self.fields['year'].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        make = cleaned_data.get('make')
        model = cleaned_data.get('model')
        year = cleaned_data.get('year')
        insurance_amount = cleaned_data.get('insurance_amount')

        if make and not make.replace(' ', '').isalpha():
            self.add_error('make', 'Марката трябва да съдържа само букви и интервали.')

        if model and not model.replace(' ', '').isalnum():
            self.add_error('model', 'Моделът трябва да съдържа само букви, цифри и интервали.')

        current_year = date.today().year
        if year:
            if year < 1900:
                self.add_error('year', 'Годината трябва да е след 1900.')
            elif year > current_year :
                self.add_error('year', f'Годината не може да бъде в бъдещето.')

        if insurance_amount and insurance_amount <= 0:
            self.add_error('insurance_amount', 'Застрахователната сума трябва да е положително число.')

        return cleaned_data


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

    def clean(self):
        cleaned_data = super().clean()
        insurance_amount = cleaned_data.get('insurance_amount')
        premium = cleaned_data.get('premium')

        if insurance_amount and insurance_amount <= 0:
            self.add_error('insurance_amount', 'Застрахователната сума трябва да е положително число.')

        if premium and premium <= 0:
            self.add_error('premium', 'Премията трябва да е положително число.')

        return cleaned_data



class CarForm(forms.ModelForm):
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
        self.fields['make'].widget.attrs['class'] = 'form-control'
        self.fields['model'].widget.attrs['class'] = 'form-control'
        self.fields['year'].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super().clean()
        make = cleaned_data.get('make')
        model = cleaned_data.get('model')
        year = cleaned_data.get('year')

        if make and not make.replace(' ', '').isalpha():
            self.add_error('make', 'Марката трябва да съдържа само букви и интервали.')

        if model and not model.replace(' ', '').isalnum():
            self.add_error('model', 'Моделът трябва да съдържа само букви, цифри и интервали.')

        current_year = date.today().year
        if year:
            if year < 1900:
                self.add_error('year', 'Годината трябва да е след 1900.')
            elif year > current_year:
                self.add_error('year', f'Годината не може да бъде в бъдещето.')

        return cleaned_data
