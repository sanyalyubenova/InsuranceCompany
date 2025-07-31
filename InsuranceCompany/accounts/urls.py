from django.urls import path,include
from InsuranceCompany.accounts.views import AppUserRegisterView, AppUserLoginView, AppUserDetailView, ProfileEditView, \
    AppUserDeleteView, AppUserLogoutView

urlpatterns = [
    path('register/', AppUserRegisterView.as_view(), name='register'),
    path('login/', AppUserLoginView.as_view(), name='login'),
    path('logout/', AppUserLogoutView.as_view(), name='logout'),
    path('profile/<int:pk>', include([
        path('', AppUserDetailView.as_view(), name='profile_details'),
        path('edit/', ProfileEditView.as_view(), name='profile_edit'),
        path('detete/', AppUserDeleteView.as_view(), name='profile_delete'),
    ]))
]
