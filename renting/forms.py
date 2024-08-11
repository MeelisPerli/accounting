from django import forms
from .models import Rental, Renter, Deposit

class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ['address', 'room_nr', 'description']

class RenterForm(forms.ModelForm):
    begin_date = forms.DateField()
    end_date = forms.DateField(required=False)
    
    class Meta:
        model = Renter
        fields = ['renter_name', 'rental', 'monthly_rent', 'monthly_communals', 'begin_date', 'end_date']
        
class DepositForm(forms.ModelForm):
    paid_back_date = forms.DateField(required=False)
    return_referral_id = forms.IntegerField(required=False)
    
    class Meta:
        model = Deposit
        fields = ['deposit_amount', 'deposit_date', 'referral_id', 'status', 'paid_back_date', 'return_referral_id']
        

class RenterDepositForm(forms.ModelForm):
    deposit_amount = forms.DecimalField(max_digits=10, decimal_places=2)
    deposit_date = forms.DateField()
    referral_id = forms.IntegerField()

    class Meta:
        model = Renter
        fields = ['renter_name', 'monthly_rent', 'monthly_communals', 'begin_date', 'deposit_amount', 'deposit_date', 'referral_id']

class RenterSearchForm(forms.Form):
    name = forms.CharField(required=False)
    address = forms.CharField(required=False)
    room_nr = forms.IntegerField(required=False)
    begin_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)