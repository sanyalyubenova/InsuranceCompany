from datetime import date, timedelta

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from InsuranceCompany.policies.models import InsurancePolicy, Claim, Discount


class PolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = ['start_date', 'end_date', 'price', 'insurance_amount', 'car']
        labels = {
            'start_date': 'Начало на полицата',
            'end_date': 'Край на полицата',
            'price': 'Премия',
            'insurance_amount': 'Застрахователна сума',
            'car': 'Автомобил',
        }
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', }),
            'insurance_amount': forms.NumberInput(attrs={'class': 'form-control', }),
            'car': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_date'].error_messages = {
            'required': 'Началната дата е задължителна.',
            'invalid': 'Моля, въведете валидна дата.',
        }
        self.fields['end_date'].error_messages = {
            'required': 'Крайната дата е задължителна.',
            'invalid': 'Моля, въведете валидна дата.',
        }
        self.fields['price'].error_messages = {
            'required': 'Премията е задължителна.',
            'invalid': 'Моля, въведете валидна сума.',
            'min_value': 'Премията трябва да е по-голяма от 0.',
        }
        self.fields['insurance_amount'].error_messages = {
            'required': 'Застрахователната сума е задължителна.',
            'invalid': 'Моля, въведете валидна сума.',
            'min_value': 'Застрахователната сума трябва да е по-голяма от 0.',
        }
        self.fields['car'].error_messages = {
            'required': 'Изборът на автомобил е задължителен.',
            'invalid': 'Моля, изберете съществуващ автомобил.',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        price = cleaned_data.get('price')
        insurance_amount = cleaned_data.get('insurance_amount')

        if start_date and end_date:
            if start_date < date.today():
                self.add_error('start_date', 'Началната дата не може да бъде в миналото.')

            if end_date <= start_date:
                self.add_error('end_date', 'Крайната дата трябва да бъде след началната дата.')

            if (end_date - start_date) > timedelta(days=365):
                self.add_error('end_date', 'Полицата не може да бъде за повече от 1 година.')

        if price and insurance_amount:
            if price <= 0:
                self.add_error('price', 'Премията трябва да е положително число.')
            if insurance_amount <= 0:
                self.add_error('insurance_amount', 'Застрахователната сума трябва да е положително число.')

        return cleaned_data

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise ValidationError('Премията трябва да е по-голяма от 0.')
        return price

    def clean_insurance_amount(self):
        insurance_amount = self.cleaned_data.get('insurance_amount')
        if insurance_amount is not None and insurance_amount <= 0:
            raise ValidationError('Застрахователната сума трябва да е по-голяма от 0.')
        return insurance_amount


class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['policy', 'amount', 'description', 'photos']
        labels = {
            'policy': 'Полица',
            'amount': 'Размер на щетата',
            'description': 'Описание',
            'photos': 'Снимка на щетата',
        }
        widgets = {
            'policy': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Опишете подробно щетата...'}),
            'photos': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['policy'].error_messages = {
            'required': 'Изборът на полица е задължителен.',
            'invalid': 'Моля, изберете съществуваща полица.',
        }
        self.fields['amount'].error_messages = {
            'required': 'Моля, въведете размер на щетата.',
            'invalid': 'Моля, въведете валидна сума.',
            'min_value': 'Размерът на щетата трябва да е по-голям от 0.',
        }
        self.fields['description'].error_messages = {
            'required': 'Описанието е задължително.',
            'max_length': 'Описанието не може да е по-дълго от 1000 символа.',
        }
        self.fields['photos'].error_messages = {
            'invalid': 'Моля, изберете валиден файл.',
            'missing': 'Моля, изберете файл.',
            'empty': 'Избраният файл е празен.',
        }

    def clean(self):
        cleaned_data = super().clean()
        policy = cleaned_data.get('policy')
        amount = cleaned_data.get('amount')
        description = cleaned_data.get('description')

        if policy and amount:
            if amount > policy.insurance_amount:
                self.add_error('amount', 'Размерът на щетата не може да надвишава застрахователната сума по полицата.')

        if description and len(description.split()) < 10:
            self.add_error('description', 'Описанието трябва да съдържа минимум 10 думи.')

        return cleaned_data

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= 0:
            raise forms.ValidationError('Размерът на щетата трябва да бъде по-голям от 0')
        return amount

    def clean_photos(self):
        photos = self.cleaned_data.get('photos')
        if photos:
            if photos.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Файлът е твърде голям. Максималният размер е 5MB.')

            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if photos.content_type not in allowed_types:
                raise forms.ValidationError('Поддържат се само JPG, PNG и GIF файлове.')

        return photos


class DiscountCreateForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['discount_type', 'percentage']

        labels = {
            'discount_type': 'Вид',
            'percentage': 'Размер'
        }
        widgets = {
            'discount_type': forms.Select(attrs={'class': 'form-control'}),
            'percentage': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '1', 'min': '1', 'max': '25', 'placeholder': '% отстъпка'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        percentage = cleaned_data.get('percentage')
        if percentage is not None:
            if percentage <= 0:
                raise forms.ValidationError('Процентът трябва да бъде по-голям от 0.')
            if percentage > 25:
                raise forms.ValidationError('Процентът не може да бъде по-голям от 25.')
        return cleaned_data


class DiscountEditForm(forms.ModelForm):
    class Meta:
        model = Discount
        fields = ['discount_type', 'percentage']

        labels = {
            'discount_type': 'Вид',
            'percentage': 'Размер'
        }
        widgets = {
            'discount_type': forms.Select(attrs={'class': 'form-control', 'disabled': 'disabled'}),
            'percentage': forms.NumberInput(
                attrs={'class': 'form-control', 'step': '1', 'min': '1', 'max': '25', 'placeholder': '% отстъпка'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        percentage = cleaned_data.get('percentage')
        if percentage is not None:
            if percentage < 1:
                self.add_error('percentage', 'Процентът трябва да бъде по-голям от 0.')
            if percentage > 25:
                self.add_error('percentage', 'Процентът не може да бъде по-голям от 25.')
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
