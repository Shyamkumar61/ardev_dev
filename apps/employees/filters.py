import django_filters
from django_filters import FilterSet, Filter
from apps.employees.models import Employee


class EmployeeFilter(django_filters.FilterSet):

    emp_id = django_filters.CharFilter(field_name='emp_id', lookup_expr='iexact')
    company = django_filters.CharFilter(field_name='current_company__client_name', lookup_expr='icontains')

    class Meta:
        model = Employee
        fields = ['emp_id', 'current_company']
