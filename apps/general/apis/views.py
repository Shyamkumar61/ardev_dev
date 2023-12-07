from rest_framework.views import Response
from rest_framework.views import  APIView
from rest_framework import generics
from rest_framework import status
from .serializers import ServiceSerializer, DesignationSerializer, ServiceOptionSerializer, BankSerializer, \
    BankOptionSerializer, DesignationOptionSerializer
from apps.general.models import Services, Designation, Banks
from apps.clients.apis.views import CustomPagination
from rest_framework.renderers import TemplateHTMLRenderer
from apps.clients.mixins import OptionMixin


class ServiceListView(generics.ListCreateAPIView):

    queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = CustomPagination


class ServiceUpdateView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Services.objects.all()
    serializer_class = ServiceSerializer
    lookup_field = 'id'


class ServiceOptionView(generics.ListAPIView):

    queryset = Services.objects.all()
    serializer_class = ServiceOptionSerializer


class DesignationView(generics.ListCreateAPIView):

    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    pagination_class = CustomPagination


class DesignationDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    lookup_field = 'id'


class DesignationOptionView(OptionMixin, generics.GenericAPIView):

    queryset = Designation.objects.all()
    serializer_class = DesignationOptionSerializer


class BankOptionView(OptionMixin, generics.GenericAPIView):

    queryset = Banks.objects.all()
    serializer_class = BankOptionSerializer


class BankView(generics.CreateAPIView):

    queryset = Banks.objects.all()
    serializer_class = BankSerializer

