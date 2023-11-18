from rest_framework import serializers
from apps.clients.models import Client
from apps.employees.models import Employee
from apps.general.models import Services, Designation
from apps.employees.apis.serializers import EmployeeListSerializer


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

