# Generated by Django 5.0.1 on 2024-04-13 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0003_alter_bankentry_bankentry_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpectedExpense',
            fields=[
                ('expectedexpense_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('entryreference_id', models.CharField(max_length=32)),
                ('rental_id', models.CharField(max_length=32)),
                ('type', models.CharField(choices=[('internet', 'Internet'), ('elekter', 'Elekter'), ('gaas', 'Gaas'), ('kommunaalid', 'Kommunaalid'), ('muu', 'Muu')], max_length=32)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
    ]
