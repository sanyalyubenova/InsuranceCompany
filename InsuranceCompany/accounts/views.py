from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import DetailView, DeleteView, UpdateView

from InsuranceCompany.accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileEditForm
from InsuranceCompany.accounts.models import Profile

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
    pass


class AppUserDetailView(DetailView):
    model = UserModel
    template_name = 'accounts/profile-details-page.html'
    context_object_name = 'user'

    def get_object(self, queryset=UserModel.objects.all()):
        pk = self.kwargs.get('pk')
        if pk:
            return UserModel.objects.get(pk=pk)
        return self.request.user


class ProfileEditView(UpdateView):
    model = Profile
    form_class = ProfileEditForm
    template_name = 'accounts/profile-edit-page.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.object.pk})


class AppUserDeleteView(DeleteView):
    model = UserModel
    template_name = 'accounts/profile-delete-page.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return redirect(self.get_success_url())
