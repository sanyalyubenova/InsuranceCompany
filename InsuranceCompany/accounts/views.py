from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views import generic as views
from django.views.generic import DetailView, DeleteView

from InsuranceCompany.accounts.forms import AppUserCreationForm, AppUserLoginForm, ProfileEditForm

UserModel = get_user_model()

# Create your views here.

class AppUserRegisterView(views.CreateView):
    model = UserModel
    form_class = AppUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')


class AppUserLoginView(LoginView):
    form_class = AppUserLoginForm
    template_name = 'accounts/login.html'


def logout(request):
    return render(request, 'accounts/logout.html')


class AppUserDetailView(DetailView):
    model = UserModel
    template_name = 'accounts/profile_details.html'


class ProfileEditView(views.UpdateView):
    model = UserModel
    form_class = ProfileEditForm
    template_name = 'accounts/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse_lazy('profile-details', kwargs={'pk': self.object.pk})


class AppUserDeleteView(DeleteView):
    model = UserModel
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self, queryset=None):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        user.delete()
        return redirect(self.get_success_url())
