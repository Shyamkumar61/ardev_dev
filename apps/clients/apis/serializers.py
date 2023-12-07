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
    service = serializers.PrimaryKeyRelatedField(queryset=Services.objects.all(), many=True)
    designation = serializers.PrimaryKeyRelatedField(queryset=Designation.objects.all(), many=True)

    class Meta:
        model = Client
        exclude = ('created', 'modified')

    def to_representation(self, instance):
        hide_relationship = self.context.get('hide_relationship', True)
        if hide_relationship and 'employee_company' in self.fields:
            del self.fields['employee_company']
        represent = super().to_representation(instance)
        represent['service'] = [{'id': value.id, 'name': value.service_name} for value in instance.service.all()]
        represent['designation'] = [{'id': value.id, 'name': value.name} for value in instance.designation.all()]
        return represent

    # def create(self, validated_data):
    #     services = validated_data.pop('service')
    #     designations = validated_data.pop('designation')
    #     client = Client.objects.create(**validated_data)
    #     client.service.set(*services)
    #     client.service.set(*designations)
    #     return client


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
        shift_type = self.validated_data.pop('shift_type')
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
