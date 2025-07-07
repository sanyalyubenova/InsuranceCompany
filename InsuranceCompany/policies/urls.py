from django.urls import path, include
from . import views

urlpatterns = [
    path('calculator/', views.calculator, name='policy_calculator'),
    path('create/', views.create_policy, name='policy_create'),
    path('<int:pk>/', include([
        path('', views.policy_detail, name='policy_detail'),
        path('edit/', views.edit_policy, name='policy_update'),
        path('delete/', views.delete_policy, name='policy_delete'),
    ])),
]