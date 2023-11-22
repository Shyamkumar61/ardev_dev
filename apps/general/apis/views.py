from rest_framework.views import Response
from rest_framework import generics
from rest_framework import status
from .serializers import ServiceSerializer, DesignationSerializer, ServiceOptionSerializer, BankSerializer
from apps.general.models import Services, Designation
from apps.clients.apis.views import CustomPagination


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


class DesignationDetailView(generics.RetrieveUpdateAPIView):

    queryset = Designation.objects.all()
    serializer_class = DesignationSerializer
    lookup_field = 'id'


