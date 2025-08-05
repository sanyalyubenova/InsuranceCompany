from datetime import datetime, date
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import QuerySet
from django.shortcuts import render, get_object_or_404
# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic import DeleteView

from InsuranceCompany.common.forms import OfferCreateForm, OfferEditForm, CarCreateForm, CarEditForm
from .models import Car, Offer
from ..accounts.models import Profile
from ..policies.models import InsurancePolicy, Discount


def home(request):
    return render(request, template_name='common/home.html')


def about(request):
    return render(request, template_name='common/about.html')


def contact(request):
    return render(request, template_name='common/contact.html')


@login_required
def offer_create(request):
    if request.method == 'POST':
        form = OfferCreateForm(request.POST)

        if form.is_valid():
            car, created = Car.objects.get_or_create(
                make=form.cleaned_data['make'],
                model=form.cleaned_data['model'],
                year=form.cleaned_data['year']
            )

            offer = Offer.objects.create(
                user=request.user,
                car=car,
                insurance_amount=form.cleaned_data['insurance_amount'],
                status='pending',
                premium=Decimal('0.00')
            )

            base_percentage = Decimal('0.05')
            vat_percentage = Decimal('1.02')
            current_year = date.today().year
            car_age = current_year - car.year
            existing_policies = InsurancePolicy.objects.filter(car=offer.car, user=offer.user).count()

            discounts = []

            if car_age < 10:
                try:
                    discounts.append(Discount.objects.get(discount_type='CAR_AGE'))
                except Discount.DoesNotExist:
                    pass

            if existing_policies == 0:
                try:
                    discounts.append(Discount.objects.get(discount_type='NEW_CLIENT'))
                except Discount.DoesNotExist:
                    pass

            if offer.insurance_amount > 10000:
                try:
                    discounts.append(Discount.objects.get(discount_type='INSURANCE_AMOUNT'))
                except Discount.DoesNotExist:
                    pass

            base_premium = offer.insurance_amount * base_percentage
            final_premium = base_premium * Decimal(1 - sum(obj.discount_percentage() for obj in discounts)) * vat_percentage
            offer.premium = final_premium
            offer.discounts.set(discounts)
            offer.save()

            return redirect('offer_details', offer_id=offer.id)
    else:
        form = OfferCreateForm()

    return render(request, 'common/offer_create.html', {'form': form})


@login_required
def offer_list(request):
    if request.user.is_staff or request.user.is_superuser:
        offers = Offer.objects.all().order_by('-created_at')
    else:
        offers = Offer.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'offers': offers
    }
    return render(request, 'common/offer_list.html', context)


@login_required
def offer_details(request, offer_id):
    offer = get_object_or_404(Offer.objects.prefetch_related('discounts'), id=offer_id)
    return render(request, 'common/offer_details.html', {'offer': offer})


@login_required
def offer_edit(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, user=request.user)

    if request.method == 'POST':
        form = OfferEditForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            return redirect('offer_details', offer_id=offer.id)
    else:
        form = OfferEditForm(instance=offer)

    return render(request, 'common/offer_edit.html', {
        'form': form,
        'offer': offer
    })


class OfferDeleteView(LoginRequiredMixin, DeleteView):
    model = Offer
    template_name = 'common/offer_delete.html'
    success_url = reverse_lazy('offer_list')
    pk_url_kwarg = 'offer_id'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


@login_required
def accept_offer(request, offer_id):
    offer = Offer.objects.get(id=offer_id, user=request.user)
    offer.accept()
    policy = InsurancePolicy.objects.create(
        user=request.user,
        car=offer.car,
        start_date=datetime.today(),
        end_date=datetime.today(),
        price=offer.premium,
        insurance_amount=offer.insurance_amount,
        offer=offer

    )
    policy.save()
    offer.created_policy = policy
    offer.save()
    return redirect('offer_list')


@login_required
def reject_offer(request, offer_id):
    offer = Offer.objects.get(id=offer_id, user=request.user)
    offer.reject()
    return redirect('offer_list')


@login_required
def profile(request):
    offers = Offer.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'offers': offers,
        'profile': request.user.profile,
        'user': request.user
    }
    return render(request, 'accounts/profile-details-page.html', context)


@login_required
def car_create(request):
    if request.method == 'POST':
        form = CarCreateForm(request.POST)

        if form.is_valid():
            car, created = Car.objects.get_or_create(
                make=form.cleaned_data['make'],
                model=form.cleaned_data['model'],
                year=form.cleaned_data['year']
            )

            car.save()

            return redirect('car_list')
    else:
        form = CarCreateForm()

    return render(request, 'common/car_create.html', {'form': form})


@login_required
def car_list(request):
    if request.user.is_staff or request.user.is_superuser:
        cars = Car.objects.all().order_by('model')
    else:
        cars = Car.objects.filter(user=request.user).order_by('model')

    context = {
        'cars': cars
    }
    return render(request, 'common/car_list.html', context)


@login_required
def car_details(request, pk):
    car = Car.objects.get(id=pk)
    return render(request, 'common/car_details.html', {'car': car})


@login_required
def car_edit(request, pk):
    car = get_object_or_404(Car, pk=pk)

    if request.method == 'POST':
        form = CarEditForm(request.POST, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_details', pk=car.pk)
    else:
        form = CarEditForm(instance=car)

    return render(request, 'common/car_edit.html', {
        'form': form,
        'car': car
    })


class CarDeleteView(LoginRequiredMixin, DeleteView):
    model = Car
    template_name = 'common/car_delete.html'
    success_url = reverse_lazy('car_list')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        return obj

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
