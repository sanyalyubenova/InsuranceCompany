from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from InsuranceCompany.policies.forms import PolicyForm
from InsuranceCompany.policies.models import InsurancePolicy
from InsuranceCompany.policies.serializers import InsurancePolicySerializer


# Create your views here.


class APIPolicyListView(APIView):
    model = InsurancePolicy
    template_name = 'policies/policy_list.html'
    context_object_name = 'policies'
    paginate_by = 10

    def get(self, request):
        policies = InsurancePolicy.objects.all()
        serializer = InsurancePolicySerializer(policies, many=True)
        return Response({"policies": serializer.data})

    def post(self, request):
        serializer = InsurancePolicySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIPolicyDetailView(APIView):
    model = InsurancePolicy
    template_name = 'policies/policy_detail.html'

    def get(self, request, pk):
        policy = InsurancePolicy.objects.get(pk=pk)
        serializer = InsurancePolicySerializer(policy)
        return Response({"policy": serializer.data})

    def put(self, request, pk):
        policy = InsurancePolicy.objects.get(pk=pk)
        serializer = InsurancePolicySerializer(policy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        policy = InsurancePolicy.objects.get(pk=pk)
        policy.delete()
        return Response(status=status.HTTP_200_OK)


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
