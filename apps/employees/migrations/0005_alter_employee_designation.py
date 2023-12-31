# Generated by Django 4.2.5 on 2023-10-13 14:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_alter_designation_options_designation_is_active_and_more'),
        ('employees', '0004_alter_employee_dob'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='designation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee', to='general.designation'),
        ),
    ]
