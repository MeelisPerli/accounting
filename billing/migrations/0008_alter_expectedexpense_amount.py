# Generated by Django 5.0.1 on 2024-04-13 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_alter_expectedexpense_contract_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectedexpense',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True),
        ),
    ]
