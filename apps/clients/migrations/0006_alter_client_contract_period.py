# Generated by Django 4.2.5 on 2023-11-17 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_rename_client_tenture_amount_client_bid_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='contract_period',
            field=models.DateField(blank=True, null=True),
        ),
    ]
