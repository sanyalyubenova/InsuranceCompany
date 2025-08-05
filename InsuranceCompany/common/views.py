from datetime import datetime, date
from decimal import Decimal

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
# Create your views here.


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from InsuranceCompany.common.forms import OfferCreateForm, OfferEditForm, CarForm
from .models import Car, Offer
from ..accounts.models import Profile
from ..policies.models import InsurancePolicy, Discount
from ..policies.serializers import CarSerializer, OfferSerializer


def home(request):
    return render(request, template_name='common/home.html')


def about(request):
    return render(request, template_name='common/about.html')


def contact(request):
    return render(request, template_name='common/contact.html')


@login_required
def offer_create(request):
    try:
        if request.method == 'POST':
            form = OfferCreateForm(request.POST)

            if form.is_valid():
                insurance_amount = form.cleaned_data['insurance_amount']
                if insurance_amount <= 0:
                    form.add_error('insurance_amount', 'Застрахователната сума не може да е по-малка от 0')
                    return render(request, 'common/offer_create.html', {'form': form})

                year = form.cleaned_data['year']
                current_year = date.today().year
                if year < 1900 or year > current_year:
                    form.add_error('year', 'Годината трябва да е между 1900 и текущата година')
                    return render(request, 'common/offer_create.html', {'form': form})

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
                final_premium = base_premium * Decimal(
                    1 - sum(obj.discount_percentage() for obj in discounts)) * vat_percentage
                offer.premium = final_premium
                offer.discounts.set(discounts)
                
                offer.save()

                return redirect('offer_details', offer_id=offer.id)
        else:
            form = OfferCreateForm()

        return render(request, 'common/offer_create.html', {'form': form})
    
    except Exception as e:
        print(f"Грешка при създаване на оферта: {e}")
        return render(request, 'common/offer_create.html', {
            'form': OfferCreateForm(),
            'error_message': 'Възникна грешка. Моля, опитайте отново.'
        })


@login_required
@permission_required('common.view_offer')
def offer_list(request):
    try:
        if request.user.is_staff or request.user.is_superuser:
            offers = Offer.objects.all().order_by('-created_at')
            context = {'offers': offers}
        else:
            offers = Offer.objects.filter(user=request.user).order_by('-created_at')
            context = {'offers': offers}
        return render(request, 'common/offer_list.html', context)
    except Exception as e:
        print(f"Грешка при зареждане на офертите: {e}")
        return render(request, 'common/offer_list.html', {
            'offers': [],
            'error_message': f'Грешка при зареждане на офертите: {str(e)}'
        })


@login_required
@permission_required('common.view_offer')
def offer_details(request, offer_id):
    try:
        if not str(offer_id).isdigit():
            return render(request, 'common/offer_details.html', {
                'error_message': 'Невалиден ID на оферта.'
            })

        offer = get_object_or_404(Offer.objects.prefetch_related('discounts'), id=offer_id)
        return render(request, 'common/offer_details.html', {'offer': offer})
    
    except Exception as e:
        print(f"Грешка при зареждане на детайлите на офертата: {e}")
        return render(request, 'common/offer_details.html', {
            'error_message': 'Възникна грешка при зареждане на детайлите на офертата.'
        })


@login_required
@permission_required('common.change_offer')
def offer_edit(request, offer_id):
    try:
        if not str(offer_id).isdigit():
            return render(request, 'common/offer_edit.html', {
                'error_message': 'Невалиден ID на оферта.'
            })

        offer = get_object_or_404(Offer, id=offer_id, user=request.user)

        if request.method == 'POST':
            form = OfferEditForm(request.POST, instance=offer)
            if form.is_valid():
                insurance_amount = form.cleaned_data['insurance_amount']
                if insurance_amount <= 0:
                    form.add_error('insurance_amount', 'Застрахователната сума не може да е по-малка от 0')
                    return render(request, 'common/offer_edit.html', {
                        'form': form,
                        'offer': offer
                    })

                form.save()
                return redirect('offer_details', offer_id=offer.id)
        else:
            form = OfferEditForm(instance=offer)

        return render(request, 'common/offer_edit.html', {
            'form': form,
            'offer': offer
        })
    
    except Exception as e:
        print(f"Error editing offer: {e}")
        return render(request, 'common/offer_edit.html', {
            'error_message': 'Възникна грешка при редактирането на офертата.'
        })


class OfferDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'common.delete_offer'
    model = Offer
    template_name = 'common/offer_delete.html'
    success_url = reverse_lazy('offer_list')
    pk_url_kwarg = 'offer_id'

    def get_object(self, queryset=None):
        try:
            obj = super().get_object(queryset)
            return obj
        except Exception as e:
            print(f"Грешка при зареждане на офертата: {e}")
            return None

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            print(f"Грешка при опит за изтриване на офертата: {e}")
            return redirect('offer_list')


@login_required
def accept_offer(request, offer_id):
    try:
        if not str(offer_id).isdigit():
            return redirect('offer_list')

        offer = Offer.objects.get(id=offer_id, user=request.user)
        offer.accept()
        start_date = datetime.today()
        end_date = start_date.replace(year=start_date.year + 1)
        
        policy = InsurancePolicy.objects.create(
            user=request.user,
            car=offer.car,
            start_date=start_date,
            end_date=end_date,
            price=offer.premium,
            insurance_amount=offer.insurance_amount,
            offer=offer
        )
        policy.save()
        offer.created_policy = policy
        offer.save()
        return redirect('offer_list')
    
    except Offer.DoesNotExist:
        print(f"Оферта {offer_id} не е намерена")
        return redirect('offer_list')
    except Exception as e:
        print(f"Грешка при приемането на офертата: {e}")
        return redirect('offer_list')


@login_required
def reject_offer(request, offer_id):
    try:
        if not str(offer_id).isdigit():
            return redirect('offer_list')

        offer = Offer.objects.get(id=offer_id, user=request.user)
        offer.reject()
        return redirect('offer_list')
    
    except Offer.DoesNotExist:
        print(f"Оферта {offer_id} не е намерена")
        return redirect('offer_list')
    except Exception as e:
        print(f"Грешка при отхвърляне на офертата: {e}")
        return redirect('offer_list')


@login_required
@permission_required('accounts.view_profile')
def profile(request):
    try:
        offers = Offer.objects.filter(user=request.user).order_by('-created_at')

        context = {
            'offers': offers,
            'profile': request.user.profile,
            'user': request.user
        }
        return render(request, 'accounts/profile-details-page.html', context)
    
    except Exception as e:
        print(f"Error loading profile: {e}")
        return render(request, 'accounts/profile-details-page.html', {
            'error_message': 'Възникна грешка при зареждане на профила.'
        })


@login_required
@permission_required('common.add_car')
def car_create(request):
    try:
        if request.method == 'POST':
            form = CarForm(request.POST)

            if form.is_valid():
                year = form.cleaned_data['year']
                current_year = date.today().year
                if year < 1900 or year > current_year:
                    form.add_error('year', 'Годината трябва да е между 1900 и текущата година')
                    return render(request, 'common/car_create.html', {'form': form})

                make = form.cleaned_data['make'].strip()
                model = form.cleaned_data['model'].strip()

                if not make or not model:
                    form.add_error(None, 'Марката и модела не могат да бъдат празни полета')
                    return render(request, 'common/car_create.html', {'form': form})

                car, created = Car.objects.get_or_create(
                    user=request.user,
                    make=make,
                    model=model,
                    year=year
                )

                car.save()
                return redirect('car_list')
        else:
            form = CarForm()

        return render(request, 'common/car_create.html', {'form': form})
    
    except Exception as e:
        print(f"Грешка при създаване на автомобил: {e}")
        return render(request, 'common/car_create.html', {
            'form': CarForm(),
            'error_message': 'Възникна грешка при създаването на автомобила. Моля, опитайте отново.'
        })


@login_required
@permission_required('common.view_car')
def car_list(request):
    try:
        if request.user.is_staff or request.user.is_superuser:
            cars = Car.objects.all().order_by('model')
        else:
            cars = Car.objects.filter(user=request.user).order_by('model')

        context = {
            'cars': cars
        }
        return render(request, 'common/car_list.html', context)
    
    except Exception as e:
        print(f"Грешка при зареждане на автомобилите: {e}")
        return render(request, 'common/car_list.html', {
            'cars': [],
            'error_message': 'Възникна грешка при зареждане на автомобилите.'
        })


@login_required
@permission_required('common.view_car')
def car_details(request, pk):
    try:
        if not str(pk).isdigit():
            return render(request, 'common/car_details.html', {
                'error_message': 'Невалиден ID на автомобил.'
            })

        car = Car.objects.get(id=pk)
        if not request.user.is_staff:
            return HttpResponseForbidden("Нямате права да видите този автомобил")
        else:
            return render(request, 'common/car_details.html', {'car': car})
    
    except Car.DoesNotExist:
        return render(request, 'common/car_details.html', {
            'error_message': 'Автомобилът не е намерен.'
        })
    except Exception as e:
        print(f"Грешка при зареждане на детайлите на автомобила: {e}")
        return render(request, 'common/car_details.html', {
            'error_message': 'Възникна грешка при зареждане на детайлите на автомобила.'
        })


@login_required
@permission_required('common.change_car')
def car_edit(request, pk):
    try:
        if not str(pk).isdigit():
            return render(request, 'common/car_edit.html', {
                'error_message': 'Невалиден ID на автомобил.'
            })

        car = get_object_or_404(Car, pk=pk)

        if request.method == 'POST':
            form = CarForm(request.POST, instance=car)
            if form.is_valid():
                year = form.cleaned_data['year']
                current_year = date.today().year
                if year < 1900 or year > current_year:
                    form.add_error('year', 'Годината трябва да е между 1900 и текущата година')
                    return render(request, 'common/car_edit.html', {
                        'form': form,
                        'car': car
                    })

                form.save()
                return redirect('car_details', pk=car.pk)
        else:
            form = CarForm(instance=car)

        return render(request, 'common/car_edit.html', {
            'form': form,
            'car': car
        })
    
    except Exception as e:
        print(f"Error editing car: {e}")
        return render(request, 'common/car_edit.html', {
            'error_message': 'Възникна грешка при редактирането на автомобила.'
        })


class CarDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = 'common.delete_car'
    model = Car
    template_name = 'common/car_delete.html'
    success_url = reverse_lazy('car_list')

    def get_object(self, queryset=None):
        try:
            obj = super().get_object(queryset)
            return obj
        except Exception as e:
            print(f"Грешка при зареждане на автомобила: {e}")
            return None

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except Exception as e:
            print(f"Грешка при изтриване на автомобила: {e}")
            return redirect('car_list')


class APICarListView(APIView):
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]

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
    permission_classes = [IsAdminUser]

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
