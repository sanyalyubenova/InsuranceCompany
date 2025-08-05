from django.shortcuts import render, redirect
from django.template.context_processors import request
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from InsuranceCompany.accounts.models import Profile
from InsuranceCompany.policies.forms import PolicyForm, DiscountForm, ClaimForm
from InsuranceCompany.policies.models import InsurancePolicy, Discount, Claim
from InsuranceCompany.policies.serializers import InsurancePolicySerializer, DiscountSerializer, ClaimSerializer, CarSerializer, OfferSerializer
from InsuranceCompany.common.models import Car, Offer


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


class APICarListView(APIView):
    def get(self, request):
        cars = Car.objects.all()
        serializer = CarSerializer(cars, many=True)
        return Response({"cars": serializer.data})

    def post(self, request):
        serializer = CarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APICarDetailView(APIView):
    def get(self, request, pk):
        car = Car.objects.get(pk=pk)
        serializer = CarSerializer(car)
        return Response({"car": serializer.data})

    def put(self, request, pk):
        car = Car.objects.get(pk=pk)
        serializer = CarSerializer(car, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        car = Car.objects.get(pk=pk)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIOfferListView(APIView):
    def get(self, request):
        offers = Offer.objects.all()
        serializer = OfferSerializer(offers, many=True)
        return Response({"offers": serializer.data})

    def post(self, request):
        serializer = OfferSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIOfferDetailView(APIView):
    def get(self, request, pk):
        offer = Offer.objects.get(pk=pk)
        serializer = OfferSerializer(offer)
        return Response({"offer": serializer.data})

    def put(self, request, pk):
        offer = Offer.objects.get(pk=pk)
        serializer = OfferSerializer(offer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        offer = Offer.objects.get(pk=pk)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIDiscountListView(APIView):
    def get(self, request):
        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return Response({"discounts": serializer.data})

    def post(self, request):
        serializer = DiscountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIDiscountDetailView(APIView):
    def get(self, request, pk):
        discount = Discount.objects.get(pk=pk)
        serializer = DiscountSerializer(discount)
        return Response({"discount": serializer.data})

    def put(self, request, pk):
        discount = Discount.objects.get(pk=pk)
        serializer = DiscountSerializer(discount, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        discount = Discount.objects.get(pk=pk)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class APIClaimListView(APIView):
    def get(self, request):
        claims = Claim.objects.all()
        serializer = ClaimSerializer(claims, many=True)
        return Response({"claims": serializer.data})

    def post(self, request):
        serializer = ClaimSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class APIClaimDetailView(APIView):
    def get(self, request, pk):
        claim = Claim.objects.get(pk=pk)
        serializer = ClaimSerializer(claim)
        return Response({"claim": serializer.data})

    def put(self, request, pk):
        claim = Claim.objects.get(pk=pk)
        serializer = ClaimSerializer(claim, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        claim = Claim.objects.get(pk=pk)
        claim.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PolicyListView(LoginRequiredMixin, ListView):
    model = InsurancePolicy
    template_name = 'policies/policy_list.html'
    context_object_name = 'policies'

    def get_queryset(self):
        if self.request.user.is_staff:
            return InsurancePolicy.objects.all()
        else:
            return InsurancePolicy.objects.filter(user=self.request.user)


class PolicyDetailView(LoginRequiredMixin, DetailView):
    model = InsurancePolicy
    template_name = 'policies/policy_detail.html'

    def get_queryset(self):
        if self.request.user.is_staff:
            return InsurancePolicy.objects.all()
        else:
            return InsurancePolicy.objects.filter(user=self.request.user)


class PolicyCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'policies.add_policy'
    model = InsurancePolicy
    form_class = PolicyForm
    template_name = 'policies/policy_create.html'
    success_url = reverse_lazy('policy_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PolicyUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'policies.change_policy'
    model = InsurancePolicy
    form_class = PolicyForm
    template_name = 'policies/policy_update.html'
    success_url = reverse_lazy('policy_list')

    def get_queryset(self):
        if self.request.user.is_staff:
            return InsurancePolicy.objects.all()
        else:
            return InsurancePolicy.objects.filter(user=self.request.user)


class PolicyDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'policies.delete_policy'
    model = InsurancePolicy
    template_name = 'policies/policy_delete.html'
    success_url = reverse_lazy('policy_list')


    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

    def delete(self, request, *args, **kwargs):
        policy = self.get_object()
        policy.delete()
        return redirect(self.get_success_url())


class DiscountListView(LoginRequiredMixin, ListView):
    # permission_required = 'discount.add_discount'
    model = Discount
    template_name = 'policies/discount_list.html'
    context_object_name = 'discounts'

    def get_queryset(self):
        return Discount.objects.all().order_by('pk')

class DiscountCreateView(LoginRequiredMixin, CreateView):
    # permission_required = 'discounts.add_discount'
    model = Discount
    form_class = DiscountForm
    template_name = 'policies/discount_create.html'
    success_url = reverse_lazy('discount_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DiscountEditView(LoginRequiredMixin, UpdateView):
    # permission_required = 'discount.change_discount'
    model = Discount
    form_class = DiscountForm
    template_name = 'policies/discount_edit.html'
    success_url = reverse_lazy('discount_list')


class DiscountDeleteView(LoginRequiredMixin, DeleteView):
    # permission_required = 'discounts.delete_discount'
    model = Discount
    template_name = 'policies/discount_delete.html'
    success_url = reverse_lazy('discount_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

    def delete(self, request, *args, **kwargs):
        discount = self.get_object()
        discount.delete()
        return redirect(self.get_success_url())


class ClaimListView(LoginRequiredMixin, ListView):
    # permission_required = 'claims.view_claim'
    model = Claim
    template_name = 'policies/claim_list.html'
    context_object_name = 'claims'

    def get_queryset(self):
        return Claim.objects.all()

class ClaimCreateView(LoginRequiredMixin, CreateView):
    # permission_required = 'claims.add_claim'
    model = Claim
    form_class = ClaimForm
    template_name = 'policies/claim_create.html'
    success_url = reverse_lazy('claim_list')

    def form_valid(self, form):
        return super().form_valid(form)

class ClaimDetailView(LoginRequiredMixin, DetailView):
    # permission_required = 'claims.view_claim'
    model = Claim
    template_name = 'policies/claim_details.html'

    def get_queryset(self):
        return Claim.objects.all()


class ClaimEditView(LoginRequiredMixin, UpdateView):
    # permission_required = 'claim.change_claim'
    model = Claim
    form_class = ClaimForm
    template_name = 'policies/claim_edit.html'
    success_url = reverse_lazy('claim_list')


class ClaimDeleteView(LoginRequiredMixin, DeleteView):
    # permission_required = 'claims.delete_claim'
    model = Claim
    template_name = 'policies/claim_delete.html'
    success_url = reverse_lazy('claim_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

    def delete(self, request, *args, **kwargs):
        claim = self.get_object()
        claim.delete()
        return redirect(self.get_success_url())
