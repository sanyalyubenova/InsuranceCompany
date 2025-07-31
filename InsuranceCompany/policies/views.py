from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from InsuranceCompany.policies.forms import PolicyForm
from InsuranceCompany.policies.models import InsurancePolicy


# Create your views here.


class PolicyListView(ListView):
    model = InsurancePolicy
    template_name = 'policies/policy_list.html'
    context_object_name = 'policies'
    paginate_by = 10


class PolicyDetailView(DetailView):
    model = InsurancePolicy
    template_name = 'policies/policy_detail.html'


class PolicyCreateView(CreateView):
    model = InsurancePolicy
    form_class = PolicyForm
    template_name = 'policies/policy_create.html'
    success_url = reverse_lazy('policy_list')


class PolicyUpdateView(UpdateView):
    model = InsurancePolicy
    form_class = PolicyForm
    template_name = 'policies/policy_update.html'


class PolicyDeleteView(DeleteView):
    model = InsurancePolicy
    success_url = reverse_lazy('policy_list')


