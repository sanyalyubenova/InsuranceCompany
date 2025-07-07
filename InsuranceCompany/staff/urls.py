from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.staff_dashboard, name='client_dashboard')
]
