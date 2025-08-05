from django import forms
from django.contrib.auth.models import User

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


class DiscountForm(forms.ModelForm):
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



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
