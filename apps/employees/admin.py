from django.contrib import admin
from apps.employees.models import Employee, EmployeeBank

# Register your models here.


admin.site.register(Employee)
admin.site.register(EmployeeBank)
