from rest_framework import serializers
from apps.general.models import Services, Designation, Banks
from rest_framework.exceptions import ValidationError


def validate_name(value):
    if not isinstance(value, str):
        raise ValidationError("No Numbers are Allowed")
    return value


class ServiceSerializer(serializers.Serializer):

    service_name = serializers.CharField(max_length=20, required=True, validators=[validate_name])

    def validate(self, data):
        service_name = data.get('service_name')
        if Services.objects.filter(service_name=service_name).exists():
            raise ValidationError("Service Already Exists")
        return data

    def create(self, validated_data):
        service = Services.objects.create(service_name=validated_data['service_name'])
        return service

    def update(self, instance, validated_data):
        instance.service_name = validated_data.get('service_name', instance.service_name)
        instance.save()
        return instance


class DesignationSerializer(serializers.Serializer):

    service = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(max_length=20, required=True, validators=[validate_name])

    def validate(self, attrs):
        name = attrs.get('name')
        if Designation.objects.filter(name=name).exists():
            raise ValidationError("Designation Already Exists")
        return attrs

    def create(self, validated_data):
        designation = Designation.objects.create(service=validated_data['service'], name=validated_data['name'])
        return designation


class EmployeeDesignation(serializers.ModelSerializer):

    class Meta:
        model = Designation
        fields = ['id', 'name']

