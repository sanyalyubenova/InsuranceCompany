from django.urls import path
from InsuranceCompany.policies.views import PolicyListView, PolicyCreateView, PolicyDetailView, PolicyUpdateView, PolicyDeleteView

urlpatterns = [
    path('', PolicyListView.as_view(), name='policy_list'),
    path('create/', PolicyCreateView.as_view(), name='policy_create'),
    path('<int:pk>/', PolicyDetailView.as_view(), name='policy_detail'),
    path('<int:pk>/edit/', PolicyUpdateView.as_view(), name='policy_update'),
    path('<int:pk>/delete/', PolicyDeleteView.as_view(), name='policy_delete'),
]
