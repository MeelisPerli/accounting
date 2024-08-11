# Generated by Django 5.0.1 on 2024-04-22 18:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0014_alter_bankentry_referral_id_and_more'),
        ('renting', '0007_alter_deposit_referral_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankentry',
            name='type',
            field=models.CharField(choices=[('rental', 'Rental'), ('deposit', 'Deposit'), ('internal_transaction', 'Internal Transaction'), ('expense', 'Expense')], default='Rent', max_length=32, null=True),
        ),
        migrations.CreateModel(
            name='RevenueReport',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('rental', 'Rental'), ('internet', 'Internet'), ('elekter', 'Elekter'), ('gaas', 'Gaas'), ('kommunaalid', 'Kommunaalid'), ('muu', 'Muu')], max_length=32)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True)),
                ('date', models.DateField()),
                ('billing_year', models.IntegerField()),
                ('bankentry_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='billing.bankentry')),
                ('deposit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='renting.deposit')),
            ],
        ),
    ]
