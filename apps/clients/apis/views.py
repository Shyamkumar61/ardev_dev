from django.shortcuts import get_object_or_404
from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer
from apps.clients.models import Client
from apps.employees.models import Employee
from apps.employees.apis.serializers import EmployeeSerializer
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from apps.clients.filters import ClientFilter
from apps.clients.apis.serializers import ShiftEmpSerializer, EmployeeCompanyEdit, clientOptionSerializer, \
                        ClientSerializer, ClientListSerializer, ShiftEmployee, ShiftEmpListSerializer
from apps.clients.mixins import OptionMixin


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_query_param = 'page_size'

    def get_paginated_response(self, data):
        response = super().get_paginated_response(data)
        page_count = response.data.get('count') // self.page_size + (1 if response.data.get('count') % self.page_size >
                                                                     0 else 0)
        return Response(OrderedDict([
            ('count', response.data.get('count')),
            ('next', response.data.get('next')),
            ('previous', response.data.get('previous')),
            ('page_count', page_count),
            ('success', True),
            ('data', data)
        ]))


class ClientListView(generics.ListAPIView):

    queryset = Client.objects.only('client_name', 'sector', 'client_phone').all()
    serializer_class = ClientListSerializer
    pagination_class = CustomPagination
    filter_class = ClientFilter

    def list(self, request, *args, **kwargs):
        data = self.get_queryset()
        filter_set = self.filter_class(request.GET, self.get_queryset())
        if filter_set.is_valid():
            data = filter_set.qs
        paginated_data = self.paginate_queryset(data)
        serializer = self.get_serializer(paginated_data, many=True)                 #need to restructure
        try:
            if serializer:
                return self.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"success": False, "data": str(e)})
        

class ClientCreateView(generics.ListCreateAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ClientDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_field = 'pk'

    def get_serializer_context(self):
        serializer_context = {
            "hide_relationship": self.request.GET.get('hide_relationship', False)
        }
        return serializer_context

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response({"success": False, "data": str(e)})

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid()
            serializer.save()
            return Response({"success": True, "data": serializer.data})
        except Exception as e:
            return Response({"success": False, "data": str(e)})


class EmployeeShiftView(generics.GenericAPIView):

    serializer_class = ShiftEmpSerializer

    def post(self, request, *args, **kwargs):
        shift_type = request.data.get('shift_type')
        if shift_type == 'Temporary':
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success": True, "data": serializer.data})
        elif shift_type == 'Permenent':
            serializer = EmployeeCompanyEdit(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success": True, "data": "Employee Shifted Successfull"})
        return Response({'success': False, "data": "Invalid Shift Type"})


class ShiftEmployeeList(generics.ListAPIView):

    queryset = ShiftEmployee.objects.filter(is_active=True)
    serializer_class = ShiftEmpListSerializer
    pagination_class = CustomPagination


class ShiftEmployeeDetails(generics.GenericAPIView):

    def get(self, request, *args, **kwargs):
        queryset = get_object_or_404(ShiftEmployee, id=60)
        emp_instance = queryset.emp_id
        emp_instance.current_company = queryset.prev_company
        queryset.is_active = False
        queryset.save()
        emp_instance.save()
        return Response({"success": True, "data": "Employee Shift Status Disabled"})


class ClientOptionView(OptionMixin, generics.GenericAPIView):

    queryset = Client.objects.all()
    serializer_class = clientOptionSerializer

