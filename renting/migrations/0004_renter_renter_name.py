# Generated by Django 5.0.1 on 2024-01-07 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('renting', '0003_remove_renter_deposit_id_remove_renter_rental_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='renter',
            name='renter_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
