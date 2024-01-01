import django_filters
from django_filters import FilterSet, Filter
from apps.employees.models import Employee


class EmployeeFilter(django_filters.FilterSet):

    emp_id = django_filters.CharFilter(field_name='emp_id', lookup_expr='iexact')
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    company = django_filters.CharFilter(field_name='current_company__id', lookup_expr='icontains')
    phone_no = django_filters.CharFilter(field_name='phone_no', lookup_expr='iexact')

    class Meta:
        model = Employee
        fields = ['emp_id', 'current_company', 'name', 'phone_no']
