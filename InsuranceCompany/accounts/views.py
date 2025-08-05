from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import DetailView, DeleteView, UpdateView
from rest_framework.permissions import IsAdminUser

from rest_framework import status

from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from InsuranceCompany.accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileEditForm
from InsuranceCompany.accounts.models import AppUser, Profile
from InsuranceCompany.accounts.serializers import UserSerializer
from InsuranceCompany.common.models import Offer
from InsuranceCompany.policies.models import InsurancePolicy

UserModel = get_user_model()


class AppUserRegisterView(views.CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        try:
            email = form.cleaned_data.get('email', '').strip()
            if not email:
                form.add_error('email', 'Имейлът не може да бъде празно поле')
                return self.form_invalid(form)
            
            password = form.cleaned_data.get('password1', '')
            if len(password) < 8:
                form.add_error('password1', 'Паролата трябва да е поне 8 символа')
                return self.form_invalid(form)
            
            return super().form_valid(form)
        except Exception as e:
            print(f"Error in user registration: {e}")
            form.add_error(None, 'Възникна грешка при регистрацията. Моля, опитайте отново.')
            return self.form_invalid(form)


class AppUserLoginView(LoginView):
    form_class = AppUserLoginForm
    template_name = 'accounts/login-page.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        try:
            email = form.cleaned_data.get('username', '').strip()
            if not email:
                form.add_error('username', 'Имейлът не може да бъде празно поле')
                return self.form_invalid(form)
            
            return super().form_valid(form)
        except Exception as e:
            print(f"Error in user login: {e}")
            form.add_error(None, 'Възникна грешка при вписването. Моля, опитайте отново.')
            return self.form_invalid(form)


class AppUserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class AppUserDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'user'

    def get_object(self, queryset=UserModel.objects.all()):
        try:
            pk = self.kwargs.get('pk')
            if pk:
                if not str(pk).isdigit():
                    return self.request.user
                return UserModel.objects.get(pk=pk)
            return self.request.user
        except UserModel.DoesNotExist:
            return self.request.user
        except Exception as e:
            print(f"Грешка при зареждане на профила: {e}")
            return self.request.user

    def get_context_data(self, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            profile, created = Profile.objects.get_or_create(user=self.request.user)
            context['profile'] = profile

            context['offers'] = Offer.objects.filter(user=self.request.user).order_by('-created_at')
            context['policies'] = InsurancePolicy.objects.filter(user=self.request.user)

            return context
        except Exception as e:
            print(f"Грешка при зареждане на профила: {e}")
            return super().get_context_data(**kwargs)


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def get_object(self, queryset=None):
        try:
            profile, created = Profile.objects.get_or_create(user=self.request.user)
            return profile
        except Exception as e:
            print(f"Грешка при зареждане на профила: {e}")
            return None

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        try:
            first_name = form.cleaned_data.get('first_name', '').strip()
            if first_name and len(first_name) > 30:
                form.add_error('first_name', 'Името не може да е по-дълго от 30 символа')
                return self.form_invalid(form)
            
            last_name = form.cleaned_data.get('last_name', '').strip()
            if last_name and len(last_name) > 30:
                form.add_error('last_name', 'Фамилията не може да е по-дълго от 30 символа')
                return self.form_invalid(form)
            
            return super().form_valid(form)
        except Exception as e:
            print(f"Грешка при обновяване на профила: {e}")
            form.add_error(None, 'Възникна грешка при обновяването на профила. Моля, опитайте отново.')
            return self.form_invalid(form)


class AppUserDeleteView(LoginRequiredMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        try:
            user = self.get_object()
            user.delete()
            return redirect(self.get_success_url())
        except Exception as e:
            print(f"Грешка при изтриването на потребителя: {e}")
            return redirect(self.get_success_url())


class APIUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = AppUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({"users": serializer.data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        user = AppUser.objects.get(pk=pk)
        serializer = UserSerializer(user)
        return Response({"user": serializer.data})

    def put(self, request, pk):
        user = AppUser.objects.get(pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = AppUser.objects.get(pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
