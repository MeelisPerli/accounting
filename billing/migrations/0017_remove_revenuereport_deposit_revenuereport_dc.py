# Generated by Django 5.0.1 on 2024-06-09 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0016_rename_bankentry_id_revenuereport_bankentry_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revenuereport',
            name='deposit',
        ),
        migrations.AddField(
            model_name='revenuereport',
            name='dc',
            field=models.CharField(max_length=1, null=True),
        ),
    ]
