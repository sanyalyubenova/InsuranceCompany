from django.urls import path, include
from . import views
from .views import OfferDeleteView, CarDeleteView

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('offer/', views.offer_create, name='offer_create'),
    path('offer/list/', views.offer_list, name='offer_list'),
    path('offer/<int:offer_id>/', views.offer_details, name='offer_details'),
    path('offer/<int:offer_id>/edit/', views.offer_edit, name='offer_edit'),
    path('offer/<int:offer_id>/delete/', OfferDeleteView.as_view(), name='offer_delete'),
    path('offer/<int:offer_id>/accept/', views.accept_offer, name='accept_offer'),
    path('offer/<int:offer_id>/reject/', views.reject_offer, name='reject_offer'),
    path('car/', views.car_create, name='car_create'),
    path('car/list/', views.car_list, name='car_list'),
    path('car/<int:pk>/', views.car_details, name='car_details'),
    path('car/<int:pk>/edit/', views.car_edit, name='car_edit'),
    path('car/<int:pk>/delete/', CarDeleteView.as_view(), name='car_delete'),

]