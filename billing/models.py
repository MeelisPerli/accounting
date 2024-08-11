from django.db import models
from django.utils import timezone
import uuid

from renting.models import Deposit


class BankEntry(models.Model):
    bankentry_id = models.CharField(max_length=64, primary_key=True)  # kande viide
    entryreferral_id = models.CharField(max_length=32)  # kande viide
    account_id = models.CharField(max_length=32)  # kliendi konto
    date = models.DateField()  # kuupäev
    dc = models.CharField(max_length=1)  # D/C
    client_name = models.CharField(max_length=128)  # kliendi nimi
    amount = models.DecimalField(max_digits=15, decimal_places=5)  # summa
    currency = models.CharField(max_length=3)  # valuuta
    memo = models.TextField()  # selgitus
    referral_id = models.CharField(max_length=32, db_index=True)  # viitenumber
    type_choices = [
        ('rental', 'Rental'),
        ('deposit', 'Deposit'),
        ('internal_transaction', 'Internal Transaction'),
        ('expense', 'Expense'),
    ]
    type = models.CharField(max_length=32, null=True, default="Rent", choices=type_choices)  # tüüp


class ExpectedExpense(models.Model):
    expectedexpense_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    referral_id = models.CharField(max_length=32, db_index=True)
    rental_id = models.CharField(max_length=32)
    type_choices = [
        ('internet', 'Internet'),
        ('elekter', 'Elekter'),
        ('gaas', 'Gaas'),
        ('kommunaalid', 'Kommunaalid'),
        ('muu', 'Muu'),
    ]
    type = models.CharField(max_length=32, choices=type_choices)
    amount = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    billing_start_date = models.DateField()
    billing_end_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.name

    def has_started(self):
        return self.billing_start_date <= timezone.now().date()

    def has_ended(self):
        if self.billing_end_date is None:
            return False
        return self.billing_end_date < timezone.now().date()

    def contract_status_color(self):
        if self.has_started() and not self.has_ended():
            return 'yellow'
        elif self.has_ended():
            return 'green'
        else:
            return 'gray'

class RevenueReport(models.Model):
    report_id = models.AutoField(primary_key=True)
    # foreign key to bank entry
    bankentry = models.ForeignKey(BankEntry, on_delete=models.CASCADE)
    type_choices = [
        ('rental', 'Rental'),
        ('internet', 'Internet'),
        ('elekter', 'Elekter'),
        ('gaas', 'Gaas'),
        ('kommunaalid', 'Kommunaalid'),
        ('muu', 'Muu'),
    ]
    type = models.CharField(max_length=32, choices=type_choices)
    dc = models.CharField(max_length=1, null=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2, blank=True, null=True)
    date = models.DateField()
    billing_year = models.IntegerField()
