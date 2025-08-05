from django.urls import path
from InsuranceCompany.policies import views
from InsuranceCompany.policies.views import PolicyListView, PolicyCreateView, PolicyDetailView, PolicyUpdateView, \
    PolicyDeleteView, DiscountListView, DiscountCreateView, DiscountEditView, DiscountDeleteView, ClaimCreateView, \
    ClaimListView, ClaimDetailView, ClaimEditView, ClaimDeleteView

urlpatterns = [
    path('', PolicyListView.as_view(), name='policy_list'),
    path('create/', PolicyCreateView.as_view(), name='policy_create'),
    path('<int:pk>/', PolicyDetailView.as_view(), name='policy_detail'),
    path('<int:pk>/edit/', PolicyUpdateView.as_view(), name='policy_update'),
    path('<int:pk>/delete/', PolicyDeleteView.as_view(), name='policy_delete'),
    path('discount/', DiscountCreateView.as_view(), name='discount_create'),
    path('discount/list/', DiscountListView.as_view(), name='discount_list'),
    path('discount/<int:pk>/edit/', DiscountEditView.as_view(), name='discount_edit'),
    path('discount/<int:pk>/delete/', DiscountDeleteView.as_view(), name='discount_delete'),
    path('claim/', ClaimCreateView.as_view(), name='claim_create'),
    path('claim/list/', ClaimListView.as_view(), name='claim_list'),
    path('claim/<int:pk>', ClaimDetailView.as_view(), name='claim_details'),
    path('claim/<int:pk>/edit/', ClaimEditView.as_view(), name='claim_edit'),
    path('claim/<int:pk>/delete/', ClaimDeleteView.as_view(), name='claim_delete'),
]
