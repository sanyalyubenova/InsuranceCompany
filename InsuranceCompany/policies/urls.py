from django.urls import path, include
from InsuranceCompany.policies import views

urlpatterns = [
    path('create/', views.policy_create, name='create_policy'),
    path('policy/<int:pk>/', include([
        path('', views.policy_details, name='profile_details'),
        path('edit/', views.policy_edit, name='profile_details'),
        path('detete/', views.policy_delete, name='profile_delete'),
    ]))
]
