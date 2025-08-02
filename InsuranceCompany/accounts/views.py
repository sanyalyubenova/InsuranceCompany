from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import DetailView, DeleteView, UpdateView

from InsuranceCompany.accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileEditForm
from InsuranceCompany.accounts.models import Profile
from InsuranceCompany.common.models import Offer
from InsuranceCompany.policies.models import InsurancePolicy

UserModel = get_user_model()


class AppUserRegisterView(views.CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register-page.html'
    success_url = reverse_lazy('login')


class AppUserLoginView(LoginView):
    form_class = AppUserLoginForm
    template_name = 'accounts/login-page.html'
    success_url = reverse_lazy('home')


class AppUserLogoutView(LogoutView):
    next_page = reverse_lazy('home')


class AppUserDetailView(LoginRequiredMixin, DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'user'

    def get_object(self, queryset=UserModel.objects.all()):
        pk = self.kwargs.get('pk')
        if pk:
            return UserModel.objects.get(pk=pk)
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure user has a profile
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        context['profile'] = profile
        
        # Get user's offers
        context['offers'] = Offer.objects.filter(user=self.request.user).order_by('-created_at')
        context['policies'] = InsurancePolicy.objects.filter(user=self.request.user)

        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def get_object(self, queryset=None):
        # Get or create profile for the current user
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.object.pk})


class AppUserDeleteView(LoginRequiredMixin, DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return redirect(self.get_success_url())
