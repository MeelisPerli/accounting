# Generated by Django 5.0.1 on 2024-04-13 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0006_rename_entryreference_id_expectedexpense_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expectedexpense',
            name='contract_end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
