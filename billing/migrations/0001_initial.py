# Generated by Django 5.0.1 on 2024-01-31 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BankEntry',
            fields=[
                ('bankentry_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_id', models.CharField(max_length=32)),
                ('date', models.DateField()),
                ('dc', models.CharField(max_length=1)),
                ('client_name', models.CharField(max_length=128)),
                ('amount', models.DecimalField(decimal_places=5, max_digits=15)),
                ('currency', models.CharField(max_length=3)),
                ('memo', models.TextField()),
                ('reference', models.CharField(max_length=32)),
            ],
        ),
    ]
