# Generated by Django 5.0.1 on 2024-04-21 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0013_rename_entryreference_id_bankentry_entryreferral_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankentry',
            name='referral_id',
            field=models.CharField(db_index=True, max_length=32),
        ),
        migrations.AlterField(
            model_name='expectedexpense',
            name='referral_id',
            field=models.CharField(db_index=True, max_length=32),
        ),
    ]
