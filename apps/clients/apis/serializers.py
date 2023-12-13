import re
import json
from rest_framework import serializers
from apps.clients.models import Client
from apps.employees.models import Employee
from apps.general.models import Services, Designation
from apps.employees.apis.serializers import EmployeeListSerializer
from apps.employees.models import ShiftEmployee
from apps.employees.models import ShiftEmployee, EmployeeHistory
from django.db import transaction
from datetime import datetime, timedelta
from rest_framework.exceptions import ValidationError
from apps.general.apis.serializers import ServiceOptionSerializer, DesignationOptionSerializer


class ClientEmployeeList(serializers.ModelSerializer):

    class Meta:
        model = Employee
        fields = ['emp_id', 'name', 'designation', 'phone_no']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['designation'] = instance.designation.name
        return response


class ClientSerializer(serializers.ModelSerializer):

    employee_company = ClientEmployeeList(many=True, read_only=True, required=False)
    service = ServiceOptionSerializer(many=True, read_only=True)
    designation = DesignationOptionSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        exclude = ('created', 'modified')

    def validate_client_name(self, value):
        if not value:
            raise serializers.ValidationError("Client Name Field Cannot Be Empty")
        elif value and not re.match(r'^[a-zA-Z\s]*$', value):
            raise serializers.ValidationError("Client Name Cannot Consist of Number and Special Char")
        print(value)
        return value

    def validate_client_phone(self, value):
        phone_number_pattern = re.compile(r'^\d{10}$')
        if not value:
            raise serializers.ValidationError("Client Phone Number Cannot be Empty")
        elif len(value) < 10 or len(value) > 10:
            raise serializers.ValidationError({"message": "Invalid phone number format. Please enter a 10-digit number."})
        elif not phone_number_pattern.match(value):
            raise serializers.ValidationError(
                {"message": "Phone Number cannot contain Alphabets or Special Charaters"})
        print(value)
        return value

    def validate_client_gst(self, value):
        if value:
            if len(value) != 15:
                raise serializers.ValidationError("Gst Number Should have 15 Characters")
            if not re.match(r'^[a-zA-Z0-9]*$', value):
                raise serializers.ValidationError("Gst Number should contain only alphanumeric characters")
            print(value)
            return value

    def validate_lut_tenure(self, value):
        if value:
            if not re.match(r'^[a-zA-Z0-9\s]*$', value):
                raise serializers.ValidationError("Lut Number should contain only alphanumeric characters")
            return value

    def validate_client_city(self, value):
        if not value:
            raise serializers.ValidationError("City Fields Cannot be Empty")
        if not re.match(r'^[a-zA-Z\s]*$', value):
            raise serializers.ValidationError("City name should contain only alphabets and spaces")
        return value

    def validate_client_pincode(self, attrs):
        pincode_pattern = re.compile(r'^\d{6}$')
        if not attrs:
            raise serializers.ValidationError("Please Enter a Pincode")
        if len(attrs) != 6:
            raise serializers.ValidationError("Please Enter a valid Pincode")
        if not pincode_pattern.match(attrs):
            raise serializers.ValidationError("Pincode must be Numbers")

    def validate_billing_type(self, value):
        if not value:
            raise serializers.ValidationError("Billing Type cannot be Empty")
        return value

    def validate_client_sector(self, value):
        if not value:
            raise serializers.ValidationError("Billing Type cannot be Empty")
        return value

    # def validate_service(self, value):
    #     if not value:
    #         raise serializers.ValidationError("Service Field cannot be empty")
    #     try:
    #         pk_list = [int(pk) for pk in json.loads(value)]
    #         return pk_list
    #     except (json.JSONDecodeError, ValueError):
    #         raise serializers.ValidationError("Invalid format for Service. Provide a list of integers.")

    def validate_designation(self, value):
        print(value)
        if not value:
            raise serializers.ValidationError("Designation Field cannot be empty")
        if value:

            try:
                value = json.loads(value)
                if not isinstance(value, list):
                    raise serializers.ValidationError("Designation should be a list")
                print(value)
                return value
            except json.JSONDecodeError as e:
                raise serializers.ValidationError("Invalid JSON format for Designation")

    def to_representation(self, instance):
        hide_relationship = self.context.get('hide_relationship', True)
        if hide_relationship and 'employee_company' in self.fields:
            del self.fields['employee_company']
        represent = super().to_representation(instance)
        # represent['service'] = [{'id': value.id, 'name': value.service_name} for value in instance.service.all()]
        # represent['designation'] = [{'id': value.id, 'name': value.name} for value in instance.designation.all()]
        return represent


class ClientListSerializer(serializers.Serializer):

    id = serializers.PrimaryKeyRelatedField(read_only=True)
    client_name = serializers.CharField(read_only=True)
    sector = serializers.CharField(read_only=True)
    client_phone = serializers.CharField(read_only=True)
    client_email = serializers.EmailField(read_only=True)
    client_logo = serializers.ImageField()
    client_employee = serializers.SerializerMethodField()

    def get_client_employee(self, instance):
        emp_count = Employee.objects.filter(current_company=instance.id).count()
        return emp_count

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['client_employee'] = self.get_client_employee(instance)
        return represent


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Services
        fields = ['id', 'service_name']


class ShiftEmpSerializer(serializers.ModelSerializer):

    Permenent = 'Permenent'
    Temporary = 'Temporary'

    shift_choice = (
        (Permenent, 'Permenent'),
        (Temporary, 'Temporary')
    )

    shift_type = serializers.ChoiceField(choices=shift_choice, write_only=True)

    class Meta:
        model = ShiftEmployee
        fields = '__all__'

    def validate(self, attrs):
        emp_id = attrs.get('emp_id')
        instance = ShiftEmployee.objects.filter(emp_id=emp_id, is_active=True)
        if instance:
            raise ValidationError({'error': "Employee Already On a Shift Please Change It"})
        return attrs

    def save(self, **kwargs):
        shift_type = self.validated_data.pop('shift_type')
        emp_instance = self.validated_data.get('emp_id')
        com_instance = self.validated_data.get('shifted_company')
        try:
            data = super().save(**kwargs)
            emp_instance.current_company = com_instance
            emp_instance.save()
            return data
        except Exception as e:
            raise serializers.ValidationError(str(e))


class EmployeeCompanyEdit(serializers.Serializer):

    emp_id = serializers.CharField(required=True, write_only=True)
    from_date = serializers.DateField()
    shifted_company = serializers.IntegerField(write_only=True, required=True)

    def save(self, **kwargs):
        # shift_type = self.validated_data.pop('shift_type')
        emp_id = self.validated_data.get('emp_id')
        company_id = self.validated_data.get('shifted_company')
        try:
            emp_instance = Employee.objects.get(emp_id=emp_id)
            client_instance = Client.objects.get(id=company_id)
            emp_history = EmployeeHistory.objects.create(emp_id=emp_instance,
                                                         joined_date=self.validated_data.get('from_date'),
                                                         prev_company=emp_instance.current_company,
                                                         last_worked=self.validated_data.get('from_date') - timedelta(days=1))
            emp_instance.current_company = client_instance
            emp_instance.joining_date = self.validated_data.get('from_date')
            emp_instance.save()
            return emp_history
        except Exception as e:
            raise serializers.ValidationError(str(e))


class clientOptionSerializer(serializers.ModelSerializer):

    value = serializers.IntegerField(source='id')
    label = serializers.CharField(source='client_name')

    class Meta:
        model = Client
        fields = ('value', 'label')


class ShiftEmpListSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShiftEmployee
        fields = ['id', 'emp_id', 'prev_company', 'shifted_company', 'from_date', 'to_date']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['emp_id'] = instance.emp_id.name
        response['prev_company'] = instance.prev_company.client_name
        response['shifted_company'] = instance.shifted_company.client_name
        return response
