# Generated by Django 5.0.1 on 2024-04-13 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0008_alter_expectedexpense_amount'),
    ]

    operations = [
        migrations.RenameField(
            model_name='expectedexpense',
            old_name='contract_end_date',
            new_name='billing_end_date',
        ),
        migrations.RenameField(
            model_name='expectedexpense',
            old_name='contract_start_date',
            new_name='billing_start_date',
        ),
    ]
