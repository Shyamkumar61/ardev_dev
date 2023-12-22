import PIL.Image
from rest_framework.views import Response
from rest_framework import generics
from rest_framework.views import APIView
from ..models import Employee, EmployeeBank
from .serializers import EmployeeSerializer, EmployeeListSerializer, EmployeeBankSerializer
from rest_framework.parsers import FileUploadParser, MultiPartParser
from PIL import Image as PILImage
from rest_framework import status
from django.shortcuts import get_object_or_404
from apps.clients.apis.views import CustomPagination
from apps.employees.filters import EmployeeFilter


class EmployeeView(generics.ListCreateAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    filter_class = EmployeeFilter
    # parser_classes = [MultiPartParser]

    def get_queryset(self):
        queryset = Employee.objects.only("name", "designation__name", "emp_id", "phone_no",
                                         "current_company__client_name").all()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        filter_set = self.filter_class(request.GET, self.get_queryset())
        if filter_set.is_valid():
            queryset = filter_set.qs
        page = self.paginate_queryset(queryset)
        serializer = EmployeeListSerializer(page, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response({"success": "New Employee Added"}, status=status.HTTP_201_CREATED)
        return Response({"error": serializer.error}, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailsView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'emp_id'

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        if not queryset:
            return Response({'success': False, 'message': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(queryset)
        return Response({'success': True, 'data': serializer.data}, status=status.HTTP_200_OK)
    
    # def put(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.update(serializer, serializer.validated_data)
    #     return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)


class EmployeeBankCreateView(generics.CreateAPIView):

    serializer_class = EmployeeBankSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response:
            return Response({"success": True, "data": response.data})
        return Response({"success": False, "error": "Invalid Data"})


class EmployeeBankDetailView(generics.GenericAPIView):

    queryset = EmployeeBank.objects.all()
    serializer_class = EmployeeBankSerializer

    def get_object(self):
        queryset = EmployeeBank.objects.get(employee__emp_id=self.kwargs.get('pk'))
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_object()
        serializer = self.get_serializer(queryset)
        return Response({"success": True, "data": serializer.data})

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': True, "data": serializer.data})
        return Response({'success': False, "error": serializer.errors})

