# Generated by Django 5.0.1 on 2024-03-24 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_bankentry_entryreference_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankentry',
            name='bankentry_id',
            field=models.CharField(max_length=64, primary_key=True, serialize=False),
        ),
    ]
