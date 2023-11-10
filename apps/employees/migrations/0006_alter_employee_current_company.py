# Generated by Django 4.2.5 on 2023-10-13 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0001_initial'),
        ('employees', '0005_alter_employee_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='current_company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_company', to='clients.client'),
        ),
    ]
