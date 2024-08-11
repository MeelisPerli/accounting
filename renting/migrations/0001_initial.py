# Generated by Django 5.0.1 on 2024-01-07 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Renter',
            fields=[
                ('renter_id', models.AutoField(primary_key=True, serialize=False)),
                ('rental_id', models.IntegerField()),
                ('deposit_id', models.IntegerField()),
                ('monthly_rent', models.DecimalField(decimal_places=2, max_digits=7)),
                ('monthly_communals', models.DecimalField(decimal_places=2, max_digits=7)),
                ('begin_date', models.DateField()),
                ('end_date', models.DateField(null=True)),
            ],
        ),
    ]
