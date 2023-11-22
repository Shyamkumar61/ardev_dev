from django.contrib import admin
from apps.employees.models import Employee, EmployeeBank, EmployeeHistory, ShiftEmployee

# Register your models here.


admin.site.register(Employee)
admin.site.register(EmployeeBank)
admin.site.register(EmployeeHistory)
admin.site.register(ShiftEmployee)
