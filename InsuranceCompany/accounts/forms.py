from datetime import date

from django import forms
from django.contrib.auth import get_user_model, login
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from InsuranceCompany.accounts.models import Profile

UserModel = get_user_model()


def validate_password_errors(password, user=None):
    try:
        validate_password(password, user)
    except ValidationError as error:
        bulgarian_errors = []
        for error_msg in error.messages:
            if "too short" in error_msg:
                bulgarian_errors.append("Паролата трябва да съдържа поне 8 символа.")
            elif "too common" in error_msg:
                bulgarian_errors.append("Паролата е твърде лесна.")
            elif "entirely numeric" in error_msg:
                bulgarian_errors.append("Паролата не може да съдържа само цифри.")
            elif "too similar" in error_msg:
                bulgarian_errors.append("Паролата е твърде подобна на личната информация.")
            else:
                bulgarian_errors.append("Паролата е невалидна.")

        if bulgarian_errors:
            raise ValidationError(bulgarian_errors)


class AppUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserModel


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Въведете вашия имейл'}),
        }
        labels = {
            'email' : 'Имейл',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'Парола'
        self.fields['password2'].label = 'Потвърждение на парола'
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Въведете парола'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Потвърдете паролата'})

        self.fields['email'].error_messages = {
            'invalid': 'Моля, въведете валиден имейл адрес.',
            'unique': 'Вече има създаден профил с този имейл адрес.',
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 != password2:
            self.add_error('password1', "Паролите не съвпадат.")
        else:
            try:
                validate_password_errors(password1, self.instance)
            except ValidationError as error:
                for msg in error.messages:
                    self.add_error('password1', msg)

        return cleaned_data


class AppUserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Имейл:",
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Въведете вашия имейл'
        })
    )
    password = forms.CharField(
        label="Парола:",
        strip=False,
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'current-password',
            'class': 'form-control',
            'placeholder': 'Въведете вашата парола'
        }),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].error_messages = {
            'invalid': 'Моля, въведете валиден имейл адрес.',
        }

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')


        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
        else:
            self.add_error('password', 'Грешен имейл или парола.')
        return self.cleaned_data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'date_of_birth']
        labels = {
            'first_name': 'Име:',
            'last_name': 'Фамилия:',
            'date_of_birth': 'Дата на раждане:',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Въведете вашето име'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Въведете вашата фамилия'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = False
        self.fields['last_name'].required = False
        self.fields['date_of_birth'].required = False

    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        date_of_birth = cleaned_data.get('date_of_birth')

        if first_name and not first_name.replace(' ', '').isalpha():
            self.add_error('first_name', 'Името трябва да съдържа само букви и интервали.')

        if last_name and not last_name.replace(' ', '').isalpha():
            self.add_error('last_name', 'Фамилията трябва да съдържа само букви и интервали.')

        if date_of_birth:
            today = date.today()
            if date_of_birth > today:
                self.add_error('date_of_birth', 'Датата на раждане не може да бъде в бъдещето.')
            elif today.year - date_of_birth.year > 120:
                self.add_error('date_of_birth', 'Моля, въведете валидна дата на раждане.')


        return cleaned_data

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name:
            return first_name.strip().title()
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name:
            return last_name.strip().title()
        return last_name
