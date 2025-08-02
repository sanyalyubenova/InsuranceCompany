from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from InsuranceCompany.policies.forms import PolicyForm
from InsuranceCompany.policies.models import InsurancePolicy


# Create your views here.


class PolicyListView(LoginRequiredMixin, ListView):
    model = InsurancePolicy
    template_name = 'policies/policy_list.html'
    context_object_name = 'policies'
    paginate_by = 10

    def get_queryset(self):
        return InsurancePolicy.objects.filter(user=self.request.user)


class PolicyDetailView(LoginRequiredMixin, DetailView):
    model = InsurancePolicy
    template_name = 'policies/policy_detail.html'

    def get_queryset(self):
        return InsurancePolicy.objects.filter(user=self.request.user)


class PolicyCreateView(LoginRequiredMixin, CreateView):
    model = InsurancePolicy
    form_class = PolicyForm
    template_name = 'policies/policy_create.html'
    success_url = reverse_lazy('policy_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PolicyUpdateView(LoginRequiredMixin, UpdateView):
    model = InsurancePolicy
    form_class = PolicyForm
    template_name = 'policies/policy_update.html'

    def get_queryset(self):
        return InsurancePolicy.objects.filter(user=self.request.user)


class PolicyDeleteView(LoginRequiredMixin, DeleteView):
    model = InsurancePolicy
    success_url = reverse_lazy('policy_list')

    def get_queryset(self):
        return InsurancePolicy.objects.filter(user=self.request.user)


