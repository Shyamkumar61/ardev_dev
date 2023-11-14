import django_filters
from django_filters import FilterSet, Filter
from apps.clients.models import Client


class ClientFilter(django_filters.FilterSet):

    client_name = django_filters.CharFilter(field_name='client_name', lookup_expr='icontains')
    sector = django_filters.CharFilter(field_name='sector', lookup_expr='icontains')

    class Meta:
        model = Client
        fields = ['client_name', 'sector']


