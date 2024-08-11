"""
URL configuration for accounting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from renting.views import home, rental_overview, rental_new, rental_detail, renter_deposit_new, renter_detail, renter_overview, renter_edit, renter_deposit_edit
from billing.views import upload_bank_entries_csv, display_bank_entries, expected_expenses, add_expected_expense, edit_expected_expense, update_bank_entries, create_and_view_revenue_report

urlpatterns = [
    #path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('rental_overview/', rental_overview, name='rental_overview'),
    path('rental/new', rental_new, name='rental_new'),
    path('rental/<int:pk>/', rental_detail, name='rental_detail'),
    path('renter_deposit/new/<int:pk>/', renter_deposit_new, name='renter_deposit_new'),
    path('renter/<int:pk>/', renter_detail, name='renter_detail'),
    path('renter_overview/', renter_overview, name='renter_overview'),
    path('renter/<int:pk>/edit/', renter_edit, name='renter_edit'),
    path('deposit/<int:pk>/edit/', renter_deposit_edit, name='renter_deposit_edit'),
    path('billing/upload_bank_csv/', upload_bank_entries_csv, name='bank_entry_csv_upload'),
    path('billing/bank_entry_viewer/', display_bank_entries, name='bank_entry_viewer'),
    path('billing/expected_expenses/', expected_expenses, name='expected_expenses'),
    path('billing/add_expected_expense/', add_expected_expense, name='add_expected_expense'),
    path('billing/edit_expected_expense/<int:expected_expense_id>/', edit_expected_expense, name='edit_expected_expense'),
    path('billing/update_bank_entries/', update_bank_entries, name='update_bank_entries'),
    path('billing/create_and_view_revenue_report/', create_and_view_revenue_report, name='create_and_view_revenue_report'),
]
