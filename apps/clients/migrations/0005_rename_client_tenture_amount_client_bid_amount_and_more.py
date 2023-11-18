# Generated by Django 4.2.5 on 2023-11-17 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0004_alter_client_client_logo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='client_tenture_amount',
            new_name='bid_amount',
        ),
        migrations.AddField(
            model_name='client',
            name='lut_tenure',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
