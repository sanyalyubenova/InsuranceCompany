from django.urls import path
from InsuranceCompany.common import views

urlpatterns = [
    path('', views.home, name='home'),
]