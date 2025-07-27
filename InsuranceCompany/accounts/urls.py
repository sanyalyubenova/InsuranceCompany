from django.urls import path,include
from InsuranceCompany.accounts import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('profile/<int:pk>', include([
        path('', views.profile_details, name='profile_details'),
        path('edit/', views.profile_edit, name='profile_details'),
        path('detete/', views.profile_delete, name='profile_delete'),
    ]))
]
