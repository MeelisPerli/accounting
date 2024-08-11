from django import forms

from billing.models import ExpectedExpense
from renting.models import Rental


class UploadFileForm(forms.Form):
    file = forms.FileField()

class RevenueReportForm(forms.Form):
    year = forms.IntegerField(label='Year', min_value=2000, max_value=2099)

class ExpectedExpenseForm(forms.ModelForm):
    rental_id = forms.ModelChoiceField(queryset=Rental.objects.all())
    contract_end_date = forms.DateField(required=False)
    amount = forms.DecimalField(max_digits=16, decimal_places=2, required=False)
    class Meta:
        model = ExpectedExpense
        fields = ['name', 'referral_id', 'rental_id', 'type', 'amount', 'billing_start_date', 'billing_end_date']

