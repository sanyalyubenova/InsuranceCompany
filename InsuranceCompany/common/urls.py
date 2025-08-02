from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('calculator/', views.insurance_calculator, name='insurance_calculator'),
    path('offer/<int:offer_id>/', views.offer_details, name='offer_details'),
    path('offer/<int:offer_id>/accept/', views.accept_offer, name='accept_offer'),
    path('offer/<int:offer_id>/reject/', views.reject_offer, name='reject_offer'),
]