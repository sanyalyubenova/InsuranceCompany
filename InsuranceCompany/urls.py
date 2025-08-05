"""
URL configuration for InsuranceCompany project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from InsuranceCompany.accounts.views import APIUserListView, APIUserDetailView
from InsuranceCompany.common.views import APICarListView, APICarDetailView, APIOfferListView, APIOfferDetailView
from InsuranceCompany.policies.views import APIPolicyListView, APIPolicyDetailView, APIDiscountListView, \
    APIDiscountDetailView, APIClaimListView, APIClaimDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        path('common/car/', APICarListView.as_view()),
        path('common/car/<int:pk>/', APICarDetailView.as_view()),
        path('common/offer/', APIOfferListView.as_view()),
        path('common/offer/<int:pk>/', APIOfferDetailView.as_view()),
        path('accounts/', APIUserListView.as_view()),
        path('accounts/<int:pk>/', APIUserDetailView.as_view()),
        path('policies/', APIPolicyListView.as_view()),
        path('policies/<int:pk>/', APIPolicyDetailView.as_view()),
        path('policies/discount/', APIDiscountListView.as_view()),
        path('policies/discount/<int:pk>/', APIDiscountDetailView.as_view()),
        path('policies/claim/', APIClaimListView.as_view()),
        path('policies/claim/<int:pk>/', APIClaimDetailView.as_view()),
    ])),
    path('', include('InsuranceCompany.common.urls')),
    path('accounts/', include('InsuranceCompany.accounts.urls')),
    path('policies/', include('InsuranceCompany.policies.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
