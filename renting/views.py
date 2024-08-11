from django.shortcuts import render, redirect, get_object_or_404
from .models import Rental, Renter, Deposit
from django.db.models import Q
from .forms import RentalForm, RenterDepositForm, RenterSearchForm, RenterForm, DepositForm
from datetime import datetime


def home(request):
    return render(request, 'home.html', {})

def rental_new(request):
    if request.method == "POST":
        form = RentalForm(request.POST)
        if form.is_valid():
            rental = form.save(commit=False)
            rental.save()
            return redirect('rental_detail', pk=rental.pk)
    else:
        form = RentalForm()
    return render(request, 'rental_new.html', {'form': form})


def renter_deposit_new(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    if request.method == "POST":
        form = RenterDepositForm(request.POST)
        if form.is_valid():
            deposit = Deposit(deposit_amount=form.cleaned_data['deposit_amount'], deposit_date=form.cleaned_data['deposit_date'], referral_id=form.cleaned_data['referral_id'])
            deposit.save()
            renter = form.save(commit=False)
            renter.rental = rental
            renter.deposit = deposit
            renter.save()
            return redirect('renter_detail', pk=renter.pk)
    else:
        form = RenterDepositForm()
    return render(request, 'renter_deposit_new.html', {'form': form, 'rental': rental})

def rental_detail(request, pk):
    rental = get_object_or_404(Rental, pk=pk)
    return render(request, 'rental_detail.html', {'rental': rental})

def renter_detail(request, pk):
    renter = get_object_or_404(Renter, pk=pk)
    return render(request, 'renter_detail.html', {'renter': renter})

def rental_overview(request):
    # get all rentals
    rentals = Rental.objects.all()
    # get all active renters where end_date is null or greater than today, if multiple renters, then use the one with the newest begin_date
    renters = Renter.objects.filter(end_date__isnull=True) | Renter.objects.filter(end_date__gt=datetime.today())
    renters = renters.order_by('begin_date')
    
    # assign renters to rentals, 
    for rental in rentals:
        rental.renter = renters.filter(rental=rental).first()
        
    return render(request, 'rental_overview.html', {'rentals': rentals})

def renter_overview(request):
    form = RenterSearchForm(request.GET)
    renters = Renter.objects.all()

    if form.is_valid():
        name = form.cleaned_data.get('name')
        if name:
            renters = renters.filter(renter_name__icontains=name)

        address = form.cleaned_data.get('address')
        if address:
            renters = renters.filter(rental__address__icontains=address)

        begin_date = form.cleaned_data.get('begin_date')
        if begin_date:
            renters = renters.filter(begin_date__gte=begin_date)

        end_date = form.cleaned_data.get('end_date')
        if end_date:
            renters = renters.filter(end_date__lte=end_date)
            
        room_nr = form.cleaned_data.get('room_nr')
        if room_nr:
            renters = renters.filter(rental__room_nr=room_nr)

    return render(request, 'renter_overview.html', {'renters': renters, 'form': form})


# EDITS

def renter_edit(request, pk):
    renter = get_object_or_404(Renter, pk=pk)
    if request.method == "POST":
        form = RenterForm(request.POST, instance=renter)
        if form.is_valid():
            renter = form.save()
            return redirect('renter_detail', pk=renter.pk)
    else:
        form = RenterForm(instance=renter)
    return render(request, 'renter_edit.html', {'form': form})

def renter_deposit_edit(request, pk):
    renter = get_object_or_404(Renter, pk=pk)
    deposit = renter.deposit
    rental = renter.rental
    
    if request.method == "POST":
        form = DepositForm(request.POST, instance=deposit)
        if form.is_valid():
            deposit = form.save()
            return redirect('renter_detail', pk=renter.pk)
    else:
        form = DepositForm(instance=deposit)

    context = {
        'form': form,
        'renter_name': renter.renter_name,
        'rental_address': rental.address,
        'room_number': rental.room_nr,
    }
    return render(request, 'deposit_edit.html', context)