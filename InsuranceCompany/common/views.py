from datetime import datetime
from decimal import Decimal

from django.shortcuts import render
# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from InsuranceCompany.policies.forms import CalculatorForm
from .models import Car, Offer
from ..accounts.models import Profile
from ..policies.models import InsurancePolicy


def home(request):
    return render(request, template_name='common/home.html')


def about(request):
    pass


def contact(request):
    pass


@login_required
def insurance_calculator(request):
    if request.method == 'POST':
        form = CalculatorForm(request.POST)

        if form.is_valid():
            car = Car.objects.create(
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

            offer.premium = offer.calculate_premium()
            offer.save()

            return redirect('offer_details', offer_id=offer.id)
    else:
        form = CalculatorForm()

    return render(request, 'common/new_offer.html', {'form': form})


@login_required
def offer_details(request, offer_id):
    offer = Offer.objects.get(id=offer_id, user=request.user)
    return render(request, 'common/offer.html', {'offer': offer})


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
    return redirect('profile_details', pk=policy.user.pk)


@login_required
def reject_offer(request, offer_id):
    offer = Offer.objects.get(id=offer_id, user=request.user)
    offer.reject()
    return redirect('insurance_calculator')


@login_required
def profile(request):
    offers = Offer.objects.filter(user=request.user).order_by('-created_at')

    context = {
        'offers': offers,
        'profile': request.user.profile,
        'user': request.user
    }
    return render(request, 'accounts/profile-details-page.html', context)
