# Generated by Django 4.2.5 on 2023-10-19 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0008_alter_employee_options_employeebank'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeebank',
            old_name='account_number',
            new_name='accountNumber',
        ),
        migrations.RenameField(
            model_name='employeebank',
            old_name='ifsc_code',
            new_name='ifscCode',
        ),
    ]