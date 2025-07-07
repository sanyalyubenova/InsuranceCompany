from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.client_dashboard, name='client_dashboard')
]
