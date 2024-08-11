from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import OuterRef, Exists, CharField
from django.db.models.functions import Cast
from .forms import UploadFileForm, ExpectedExpenseForm, RevenueReportForm
from .models import BankEntry, ExpectedExpense, RevenueReport
import csv

from renting.models import Deposit


def _handle_uploaded_lhv_csv(f):
    content = f.read().decode('utf-8-sig')
    reader = csv.reader(content.splitlines())
    header = next(reader)  # Get the header row
    # Create a mapping from CSV column names to BankEntry field names
    field_mapping = {
        'Konto teenusepakkuja viide': 'bankentry_id',
        'Kande viide': 'entryreferral_id',
        'Kliendi konto': 'account_id',
        'Kuupäev': 'date',
        'Deebet/Kreedit (D/C)': 'dc',
        'Saaja/maksja nimi': 'client_name',
        'Summa': 'amount',
        'Valuuta': 'currency',
        'Selgitus': 'memo',
        'Viitenumber': 'referral_id',
    }
    added_rows = 0
    total_rows = 0
    for row in reader:
        total_rows += 1
        # Create a dictionary from the row using the field mapping
        data = {field_mapping[column]: value for column, value in zip(header, row) if column in field_mapping}
        _, created = BankEntry.objects.get_or_create(bankentry_id=data['bankentry_id'], defaults=data)
        if created:
            added_rows += 1
        else:
            print(f"Bank entry already exists: {data}")
    return added_rows, total_rows


def update_bank_entries(request):
    if request.method == 'POST':
        # update all bank entries that have a deposit with the same referral_id
        BankEntry.objects.filter(entryreferral_id__in=Deposit.objects.values('referral_id')).update(type='deposit')
        return redirect('bank_entry_viewer')


def upload_bank_entries_csv(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            added_rows, total_rows = _handle_uploaded_lhv_csv(request.FILES['file'])
            return render(request, 'bank_entry_upload_success.html',
                          {'added_rows': added_rows, 'total_rows': total_rows})
    else:
        form = UploadFileForm()
    return render(request, 'bank_entry_upload.html', {'form': form})


def display_bank_entries(request):
    if request.method == 'POST':
        selected_type = request.POST.get('type')
        selected_entries = request.POST.getlist('selected_entries')
        print(selected_type)
        print(selected_entries)
        BankEntry.objects.filter(bankentry_id__in=selected_entries).update(type=selected_type)
        return redirect('bank_entry_viewer')
    else:
        bank_entries = BankEntry.objects.all()

        # Get filter parameters from request
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        dc = request.GET.get('dc')
        amount = request.GET.get('amount')
        currency = request.GET.get('currency')
        client_name = request.GET.get('client_name')
        type = request.GET.get('type')

        # Apply filters if parameters are provided
        if start_date and end_date:
            bank_entries = bank_entries.filter(date__range=[start_date, end_date])
        if dc:
            bank_entries = bank_entries.filter(dc=dc)
        if amount:
            bank_entries = bank_entries.filter(amount=amount)
        if currency:
            bank_entries = bank_entries.filter(currency=currency)
        if client_name:
            bank_entries = bank_entries.filter(client_name__icontains=client_name)
        if type and type != 'all':
            bank_entries = bank_entries.filter(type=type)

        # sort by date
        bank_entries = bank_entries.order_by('date')

        return render(request, 'bank_entry_viewer.html',
                      {'bank_entries': bank_entries, 'type_choices': BankEntry.type_choices})


def expected_expenses(request):
    expected_expenses = ExpectedExpense.objects.all()
    return render(request, 'expected_expenses.html', {'expected_expenses': expected_expenses})


def add_expected_expense(request):
    if request.method == 'POST':
        form = ExpectedExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expected_expenses')
    else:
        form = ExpectedExpenseForm()

    return render(request, 'expected_expenses_add.html', {'form': form})


def edit_expected_expense(request, expected_expense_id):
    expected_expense = get_object_or_404(ExpectedExpense, pk=expected_expense_id)
    if request.method == 'POST':
        form = ExpectedExpenseForm(request.POST, instance=expected_expense)
        if form.is_valid():
            form.save()
            return redirect('expected_expenses')
    else:
        form = ExpectedExpenseForm(instance=expected_expense)
    return render(request, 'expected_expenses_edit.html', {'form': form})


def create_and_view_revenue_report(request):
    if request.method == 'POST':
        form = RevenueReportForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data['year']

            with connection.cursor() as cursor:
                query = f"""
                WITH
                revenue AS (
                    SELECT 
                        be.bankentry_id,
                        be.amount - COALESCE(d.deposit_amount, 0) AS amount,
                        'rental' AS type,
                        be.date,
                        'C' AS dc,
                        {year} AS billing_year
                    FROM billing_bankentry be
                    LEFT JOIN renting_deposit d ON be.entryreferral_id = d.referral_id
                    WHERE (date_part('year', be.date) = {year} or ({year} = 2023 and date_part('year', be.date) = 2022))
                        AND be.type in ('rental', 'deposit') AND be.dc = 'C'
                ),
                costs AS (
                    SELECT 
                        be.bankentry_id,
                        abs(be.amount),
                        COALESCE(ee.type, be.type) AS type,
                        be.date,
                        'D' AS dc,
                        {year} AS billing_year
                    FROM billing_bankentry be
                    LEFT JOIN billing_expectedexpense ee ON be.referral_id = ee.referral_id 
                        and be.date >= ee.billing_start_date and COALESCE(ee.billing_end_date, '9999-12-31') > be.date
                    WHERE (date_part('year', be.date) = {year} or ({year} = 2023 and date_part('year', be.date) = 2022))
                        AND (be.type = 'expense' OR (be.type = 'rental' AND ee.referral_id is not null))
                ),
                final AS (
                    SELECT * FROM revenue
                    UNION ALL
                    SELECT * FROM costs
                )
                SELECT * FROM final WHERE amount != 0 order by date
                """

                cursor.execute(query)
                rows = cursor.fetchall()

                for row in rows:
                    RevenueReport.objects.create(
                        bankentry_id=row[0],
                        type=row[2],
                        amount=row[1],
                        date=row[3],
                        dc=row[4],
                        billing_year=row[5]
                    )

            return redirect('create_and_view_revenue_report')
    else:
        form = RevenueReportForm()

    revenue_reports = RevenueReport.objects.all()
    return render(request, 'revenue_report.html', {'form': form, 'revenue_reports': revenue_reports})
