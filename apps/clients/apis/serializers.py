from rest_framework import serializers
from apps.clients.models import Client
from apps.employees.models import Employee
from apps.general.models import Services, Designation
from apps.employees.apis.serializers import EmployeeListSerializer


class ClientSerializer(serializers.ModelSerializer):

    service = serializers.PrimaryKeyRelatedField(queryset=Services.objects.all(), many=True)
    designation = serializers.PrimaryKeyRelatedField(queryset=Designation.objects.all(), many=True)

    class Meta:
        model = Client
        exclude = ('created', 'modified')

    def get_employee(self, obj):
        if self.context.get('hide_employee', True):
            return None
        else:
            return EmployeeListSerializer(obj.employee, many=True, context=self.context).data

    def to_representation(self, instance):
        represent = super().to_representation(instance)
        represent['service'] = [{'id': value.id, 'name': value.service_name} for value in instance.service.all()]
        represent['designation'] = [{'id': value.id, 'name': value.name} for value in instance.designation.all()]
        return represent

    # def create(self, validated_data):
    #     services = validated_data.pop('service')
    #     designations = validated_data.pop('designations')
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

