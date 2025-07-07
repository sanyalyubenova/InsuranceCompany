from django.shortcuts import render


# Create your views here.

def register(request):
    return render(request, 'accounts/register.html')


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'accounts/logout.html')


def profile_details(request):
    return render(request, 'accounts/profile_details.html')


def edit_profile(request):
    return render(request, 'accounts/profile_edit.html')


def delete_profile(request):
    return render(request, 'accounts/profile_delete.html')
